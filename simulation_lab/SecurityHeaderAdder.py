# This middleware adds various security related headers to every response
# We are taking a whitelist approach and only allowing things we need
def SecurityHeaderAdder(get_response):
    def middleware(request):
        response = get_response(request)
        # content security policy is set to allow interacting with our own domain but no others. It also disallows inline scripts and styles
        # We are not explicitly specififying properties that fallback to default-src when specificying would have no effect
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
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
        
        # disables referers from being sent to other domains, ideally we would disable referrer totally but can't for django csrf protection
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
        response["Referrer-Policy"] = "same-origin"  # can't set to no-referrer because of csrf tokens

        # we do not allow cross site requests
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy
        response["Cross-Origin-Resource-Policy"] = "same-origin"

        # requires that the tls cert the page is served with is published in a trusted certificate transparency log
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT
        # response["Expect-CT"] = "max-age=86400, enforce" enable after verifying hosting is in CT log

        # requires the domain and all subdomains be served over https (doesn't effect localhost)
        # it has a long period and may be preloaded so can't be easily disabled
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
        response["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

        # disabled js access to all supporting api's we don't use
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
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

        # prevent some browsers from guessing content type
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
        response["X-Content-Type-Options"] = "nosniff"

        # prevent the page from being embedded in legacy browers iframe
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
        response["X-Frame-Options"] = "deny" # also set by CSP, for legacy browers

        # enable stricter xss protection mechanisms in legacy browsers
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
        response["X-XSS-Protection"] = "1; mode=block" # also set by CSP, for legacy browers
        return response

    return middleware
