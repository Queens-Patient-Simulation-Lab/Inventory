def SecurityHeaderAdder(get_response):
    def middleware(request):
        response = get_response(request)
        response["Content-Security-Policy"] = (
            "sandbox allow-downloads-without-user-activation allow-forms allow-same-origin allow-scripts; " +
            "upgrade-insecure-requests; " +
            "default-src 'none'; " +
            "form-action 'self'; " +
            "plugin-types 'none'; " +
            "frame-ancestors 'none'; " +
            "img-src 'self'; " +
            "connect-src 'self'; " +
            "script-src 'self'; " +
            "style-src 'self'")
        return response

    return middleware
