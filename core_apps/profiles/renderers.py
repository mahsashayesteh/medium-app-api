import json
from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        # بررسی می‌کنیم که renderer_context وجود داشته باشد
        
        if renderer_context is not None:
            
            try:
                if isinstance(renderer_context, str):
                  
                    renderer_context = json.loads(r"{}".format(renderer_context) )
            except json.JSONDecodeError:
                raise ValueError("invalid renderer_context format")
            response = renderer_context.get("response")
            if response is not None:
                status_code = response.status_code
            else:
                status_code = 200
            
        else:
            status_code = 200
            
        error = data.get('errors', None)

        if error is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data})
        

class ProfilesJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        if renderer_context is not None:
            
            try:
                if isinstance(renderer_context, str):
                    print(media_type)
                    print(renderer_context)
                    print("44444444444444444444444444444")
                    renderer_context = json.loads(r"{}".format(renderer_context) )
            except json.JSONDecodeError:
                raise ValueError("invalid renderer_context format")
            response = renderer_context["response"]
            if response is not None:
                status_code = response.status_code
            else:
                status_code = 200
            
        else:
            status_code = 200
        if isinstance(data, dict) and data.get("errors") :
           error = data["errors"]
        else:
            error = None

        if error is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code":status_code, "profiles": data})
        

