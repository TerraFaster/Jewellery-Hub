from fastapi import Request

from application import config


# FastAPI url_for method fix for servers
# def request_url_for(self, name: str, **path_params) -> str:
#     router = self.scope["router"]
#     url_path = router.url_path_for(name, **path_params)
#     path = url_path.make_absolute_url(base_url=self.base_url).split("/")

#     return (
#         f"{path[0]}//{config.SERVER_NAME}/" +
#         "/".join(path[3:])
#     )

# setattr(Request, "url_for", request_url_for)
