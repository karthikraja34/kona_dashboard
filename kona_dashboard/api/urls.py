from django.urls import include, path

urlpatterns = [
    path(
        "v1/",
        include(("kona_dashboard.api.v1.urls", "kona_dashboard.api"), namespace="v1"),
    ),
]
