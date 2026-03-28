import dagger
from dagger import dag, function, object_type

@object_type
class DockerColors:

    @function
    async def build(self, source: dagger.Directory, color: str = "blue") -> list[dagger.Container]:
        color_arg = "COLOR=%s" % color
        print("Building image for color %s" % color)
        img = (
            dag.docker()
            .build(
                dir=source,
                platform=[
                  dagger.Platform("linux/amd64"),
                  dagger.Platform("linux/arm64")
                ],
                args=[color_arg]
            )
        )
        return [
          img.image(platform=dagger.Platform("linux/amd64")),
          img.image(platform=dagger.Platform("linux/arm64"))
        ]

    @function
    async def ci(self, source: dagger.Directory) -> None:
        colors = [
          "blue",
          "brown",
          "gold",
          "gray",
          "green",
          "lime",
          "orange",
          "pink",
          "purple",
          "red",
          "silver",
          "teal",
          "white",
          "yellow"
        ]

        for color in colors:
            print("building docker image for variant=%s" % color)
            variants = await self.build(source=source, color=color)
            await dag.container().publish("webofmars/colors:%s" % color, platform_variants=variants)
