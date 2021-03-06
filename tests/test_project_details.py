from server.project_details import project_user_from_jwt


def test_project_user_from_jwt():
    # Generated by http://jwtbuilder.jamiekurtz.com/
    # Contains custom claims preferred_username, email and Role
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJKV1QgQnVpbGRlciIsImlhdCI6MTY0Mzg3NjY4NiwiZXhwIjoxNjc1ND" \
            "EyNjg2LCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJqckBzc2Iubm8iLCJuYW1lIjoiSm9obm55IFJvY2tldCIsInByZWZlc" \
            "nJlZF91c2VybmFtZSI6ImpyQHNzYi5ubyIsImVtYWlsIjoiam9obm55LnJvY2tldEBzc2Iubm8iLCJSb2xlIjpbIlByb2plY3QgQWRt" \
            "aW5pc3RyYXRvciIsIlVzZXIiXX0.gssgqBXvusCRugBywNEW0_vXPjTJqRwQUmJ3Mf8sCn4"
    project_user = project_user_from_jwt(token)
    assert project_user.name == "Johnny Rocket"
    assert project_user.email == "johnny.rocket@ssb.no"
    assert project_user.email_short == "jr@ssb.no"

    # Missing preferred_username
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJKV1QgQnVpbGRlciIsImlhdCI6MTY0Mzg3NjY4NiwiZXhwIjoxNjc1ND" \
            "EyNjg2LCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJqckBzc2Iubm8iLCJuYW1lIjoiSm9obm55IFJvY2tldCIsImVtYWlsI" \
            "joiam9obm55LnJvY2tldEBzc2Iubm8ifQ.X1FuLwIff1HYHmk_skkD5rPgjbf3DnZFzQbMzaq8i7A"
    project_user = project_user_from_jwt(token)
    assert project_user.name == "Johnny Rocket"
    assert project_user.email == "johnny.rocket@ssb.no"
    assert project_user.email_short == "johnny.rocket@ssb.no"
