This command returns the client ID we are redirecting our
[tracking](../topics/client-side-caching.md) notifications to. We set a client
to redirect to when using [`CLIENT TRACKING`](client-tracking.md) to enable tracking. However in
order to avoid forcing client libraries implementations to remember the
ID notifications are redirected to, this command exists in order to improve
introspection and allow clients to check later if redirection is active
and towards which client ID.

## Reply

One of the following:

* Integer: `0` when not redirecting notifications to any client.
* Integer: `-1` if client tracking is not enabled.
* Integer: the ID of the client to which notification are being redirected.
