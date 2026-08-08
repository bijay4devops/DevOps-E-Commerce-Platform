from app import create_app


def test_root_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200

        data = response.get_json()

        assert data["application"] == "DevOps E-Commerce Platform"
        assert data["status"] == "UP"
        assert data["version"] == "1.0.0"


def test_health_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/health")

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "healthy"


def test_auth_health_endpoint():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/api/auth/health")

        assert response.status_code == 200

        data = response.get_json()

        assert data["status"] == "UP"
        assert data["application"] == "DevOps E-Commerce Platform"
        assert data["version"] == "1.0.0"
