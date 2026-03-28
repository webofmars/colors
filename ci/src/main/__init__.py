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
          "aqua", "aquamarine", "azure",
          "beige", "black", "blue", "brown",
          "chartreuse", "chocolate", "coral", "crimson", "cyan",
          "darkblue", "darkgreen", "darkorange", "darkred", "darkviolet",
          "deeppink", "dodgerblue",
          "forestgreen", "fuchsia",
          "gold", "goldenrod", "gray", "green",
          "hotpink",
          "indigo", "ivory",
          "khaki",
          "lavender", "lightblue", "lightcoral", "lightgreen", "lightpink", "lightyellow",
          "lime", "limegreen",
          "magenta", "maroon", "mediumblue", "mediumorchid", "mediumpurple", "mintcream",
          "navy",
          "olive", "orange", "orangered", "orchid",
          "peachpuff", "peru", "pink", "plum", "purple",
          "red", "rosybrown", "royalblue",
          "salmon", "sandybrown", "seagreen", "sienna", "silver", "skyblue", "snow",
          "tan", "teal", "thistle", "tomato", "turquoise",
          "violet",
          "wheat", "white",
          "yellow", "yellowgreen"
        ]

        for color in colors:
            print("building docker image for variant=%s" % color)
            variants = await self.build(source=source, color=color)
            await dag.container().publish("webofmars/colors:%s" % color, platform_variants=variants)
