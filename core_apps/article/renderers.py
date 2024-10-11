import json
from rest_framework.renderers import JSONRenderer

class ArticleJSONRenderer(JSONRenderer):
     charset = "utf-8"

     def render(self, data, media_type=None, renderer_context=None):
        
        if renderer_context is not None:
            
            try:
               
               if isinstance(renderer_context, str):
                   renderer_context = json.loads(r"{}".format(renderer_context))
            except json.JSONDecodeError:
                raise ValueError("Invalid renderer_context format")
            
            response = renderer_context.get("response")
            if response is not None:
                status_code = response.status_code
                if status_code == 204:
                    return b''
            else:
                status_code = 200
        else:
            status_code = 200
        
        if data is None:
          data = {}
        error = data.get('error', None)

        if error is not None:
            return super(ArticleJSONRenderer, self).renderer(data)
        return json.dumps({"status_code":status_code, "article": data})


class ArticlesJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def renderer(self, data, media_type=None, renderer_context=None):
        
        if renderer_context is not None:
            try:
                if isinstance(renderer_context, str):
                    renderer_context = json.loads(r"{}".format(renderer_context))
            except json.JSONDecodeError:
                raise ValueError("Invalid renderer_context format")
            
            response = renderer_context.get("response")
            if response is not None:
               status_code = response.status_code
            else:
                status_code = 200
        status_code = 200
        error = data.get('error', None)

        if error is not None:
            return super(ArticlesJSONRenderer, self).renderer(data)
        return json.dumps({"status_code": status_code, "articles":data})


