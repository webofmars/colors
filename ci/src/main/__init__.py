import json
import dagger
from dagger import dag, function, object_type

@object_type
class DockerColors:

    @function
    async def build(self, source: dagger.Directory , color: str = "blue") -> list[dagger.Container]:
        color_arg = "COLOR=%s" % color
        platform = [dagger.Platform("linux/amd64"), dagger.Platform("linux/arm64")]
        dag = dagger.Client()
        print("Building image for color %s" % color)
        print("Directory: %s" % source.id)
        img = (
            dag.docker()
            .build(
                dir=source,
                platform=platform,
                args=[color_arg]
            )
        )
        print("Img: %s" % repr(img.image()))
        return [img.image(platform=platform)]

    @function
    async def push(self, image: dagger.Container) -> None:
        print("Pushing image %s" % image.id)
        dag = dagger.Client()
        dag.docker().push(image)

    @function
    # login to the docker registry
    async def login(self) -> None:
        dag = dagger.Client()
        dag.docker().login()

    @function
    def ci(self, source: dagger.Directory) -> None:
        colors = ["red", "green", "blue", "yellow", "purple"]
        platforms = [
            dagger.Platform("linux/amd64"), dagger.Platform("linux/arm64")
        ]
        for color in colors:
            self.build(self, source=source, color=color, platforms=platforms)
