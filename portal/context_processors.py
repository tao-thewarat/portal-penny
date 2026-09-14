def discord_profile(request):
    """Expose the logged-in user's Discord name and avatar as `profile`."""
    user = getattr(request, "user", None)

    if user is None or not user.is_authenticated:
        return {}

    account = user.socialaccount_set.filter(provider="discord").first()

    if account is None:
        return {
            "profile": {
                "name": user.get_username(),
                "username": None,
                "avatar_url": None,
            },
        }

    data = account.extra_data

    return {
        "profile": {
            "name": data.get("global_name")
            or data.get("username")
            or user.get_username(),
            "username": data.get("username"),
            # None when the user has no custom Discord avatar
            "avatar_url": account.get_avatar_url(),
        },
    }
