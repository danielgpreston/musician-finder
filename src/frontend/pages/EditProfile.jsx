import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import "./EditProfile.css";

function EditProfile() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState(null);
  const [options, setOptions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      const token = sessionStorage.getItem("authToken");

      if (!token) {
        navigate("/login", { replace: true });
        return;
      }

      try {
        const headers = {
          Authorization: `Token ${token}`
        };

        const [profileResponse, optionsResponse] = await Promise.all([
          fetch("/api/profiles/me/", {
            headers,
            signal: controller.signal
          }),
          fetch("/api/options/", {
            headers,
            signal: controller.signal
          })
        ]);

        if (profileResponse.status === 401 ||
            optionsResponse.status === 401) {
          sessionStorage.removeItem("authToken");
          navigate("/login", { replace: true });
          return;
        }

        if (!profileResponse.ok || !optionsResponse.ok) {
          throw new Error("Failed to load profile data.");
        }

        const profileData = await profileResponse.json();
        const optionsData = await optionsResponse.json();

        setFormData(profileData);
        setOptions(optionsData);

      } catch (err) {
        if (err.name !== "AbortError") {
          setError(err.message);
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => controller.abort();
  }, [navigate]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <main className="edit-profile-page">
      <section className="edit-profile-card">
        <header className="edit-profile-header">
          <Link to="/profile/me" className="edit-profile-back">
            <ArrowLeft size={22} />
          </Link>

          <h1>Edit Profile</h1>
        </header>

        <p>Customize your musician profile.</p>

        <h2>Profile Data</h2>
        <pre>{JSON.stringify(formData, null, 2)}</pre>

        <h2>Available Options</h2>
        <pre>{JSON.stringify(options, null, 2)}</pre>

      </section>
    </main>
  );
}

export default EditProfile;