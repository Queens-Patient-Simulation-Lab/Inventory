def SecurityHeaderAdder(get_response):
    def middleware(request):
        response = get_response(request)
        response["Content-Security-Policy"] = (
            "sandbox allow-downloads-without-user-activation allow-forms allow-same-origin allow-scripts; " +
            "upgrade-insecure-requests; " +
            "default-src 'none'; " +
            "form-action 'self'; " +
            "frame-ancestors 'none'; " +
            "img-src 'self'; " +
            "connect-src 'self'; " +
            "script-src 'self'; " +
            "style-src 'self'")
        response["Referrer-Policy"] = "same-origin"  # can't set to no-referrer because of csrf tokens
        response["Cross-Origin-Resource-Policy"] = "same-origin"
        # response["Expect-CT"] = "max-age=86400, enforce" enable after verifying hosting is in CT log
        response["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response["Feature-Policy"] = (
            "accelerometer 'none'; " +
            "ambient-light-sensor 'none';" +
            "autoplay 'none'; " +
            "battery 'none'; " +
            "display-capture 'none'; " +
            "document-domain 'none'; " +
            "encrypted-media 'none'; " +
            "geolocation 'none'; " +
            "gyroscope 'none'; " +
            "layout-animations 'none'; " +
            "fullscreen 'none'; " +
            "magnetometer 'none'; " +
            "microphone 'none'; " +
            "midi 'none'; " +
            "navigation-override 'none'; " +
            "payment 'none'; " +
            "picture-in-picture 'none'; " +
            "publickey-credentials 'none'; " +
            "usb 'none'; " +
            "wake-lock 'none'; " +
            "xr-spatial-tracking 'none'; " +
            "oversized-images 'self'; " +  # in case we have to deal with migrating to uploading large/legacy images
            "legacy-image-formats 'self'; " +
            "camera 'self'"  # for adding images from a phone
        )
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "deny" # also set by CSP, for legacy browers
        response["X-XSS-Protection"] = "1; mode=block" # also set by CSP, for legacy browers
        return response

    return middleware
