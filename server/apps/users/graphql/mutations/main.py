from apps.users.graphql.mutations import auth, me, register


class UsersMutations:
    """A class represents list of available mutations."""

    login = auth.LoginMutation.Field()
    logout = auth.LogoutMutation.Field()

    register = register.RegisterMutation.Field()
    update_me = me.UpdateMeMutation.Field()

    social_login = auth.SocialLoginMutation.Field()
    social_login_complete = auth.SocialLoginCompleteMutation.Field()
