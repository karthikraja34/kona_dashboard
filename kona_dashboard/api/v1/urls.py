from django.urls import include, path

urlpatterns = [
    path(
        "checkins/",
        include(
            ("kona_dashboard.api.v1.checkins.urls", "kona_dashboard.api.v1.checkins"),
            namespace="checkins",
        ),
    ),
]
