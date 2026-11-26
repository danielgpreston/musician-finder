import { MapPin, CalendarDays, ExternalLink, Camera, Video, Globe } from "lucide-react";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./Profile.css";

function Profile() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [musician, setMusician] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function fetchProfile() {
      setLoading(true);
      setError("");
      setMusician(null);

      const token = sessionStorage.getItem("authToken");

      if (!token) {
        navigate("/login", { replace: true });
        return;
      }

      try {
        const response = await fetch(
          `/api/profiles/${encodeURIComponent(id)}/`,
          {
            headers: {
              Authorization: `Token ${token}`
            },
            signal: controller.signal
          }
        );

        if (response.status === 401) {
          sessionStorage.removeItem("authToken");
          navigate("/login", { replace: true });
          return;
        }

        if (response.status === 404) {
          throw new Error("Musician not found.");
        }

        if (!response.ok) {
          throw new Error("Unable to load profile.");
        }

        const data = await response.json();
        setMusician(data);

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

    fetchProfile();

    return () => controller.abort();
  }, [id, navigate]);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  const name = musician.display_name || musician.username;

  const location = [musician.city, musician.state].filter(Boolean).join(", ");

  const experience = musician.experience_level.charAt(0).toUpperCase() + musician.experience_level.slice(1);

  return (
    <main className="profile-page">
      <section className="profile-card">

        <header className="profile-header">
          <div className="profile-avatar">
            {name.charAt(0).toUpperCase()}
          </div>

          <div>
            <h1>{name}</h1>

            <p className = "profile-muted">
              @{musician.username}
            </p>

            <p className="profile-location">
              <MapPin size={16} />
              {location || "Location not specified"}
            </p>
          </div>
        </header>
        
        <section className="profile-section">
          <h2>About</h2>
          <p>{musician.bio || "No bio available."}</p>
        </section>

        <section className="profile-section">
          <h2>Instruments</h2>

          {musician.instruments.length > 0 ? (
            <div className="profile-tags">
              {musician.instruments.map((instrument) => (
                <span className="profile-tag" key={instrument}>
                  {instrument}
                </span>
              ))}
            </div>
          ) : (
            <p className="profile-muted">
              No instruments listed.
            </p>
          )}
        </section>

        <section className="profile-section">
          <h2>Genres</h2>

          {musician.genres.length > 0 ? (
            <div className="profile-tags">
              {musician.genres.map((genre) => (
                <span className="profile-tag" key={genre}>
                  {genre}
                </span>
              ))}
            </div>
          ) : (
            <p className="profile-muted">
              No genres listed.
            </p>
          )}
        </section>

        {/* Experience */}
        <section className="profile-section">
          <h2>Experience</h2>

          <div className="profile-experience">
            <CalendarDays size={18} />
            <span>{experience}</span>
          </div>
        </section>

        <section className="profile-section">
          <h2>Looking For</h2>

          {musician.looking_for?.length > 0 ? (
            <div className="profile-tags">
              {musician.looking_for.map((instrument) => (
                <span className="profile-tag" key={instrument}>
                  {instrument}
                </span>
              ))}
            </div>
          ) : (
            <p className="profile-muted">
              Not currently looking for collaborators.
            </p>
          )}
        </section>

        <section className="profile-section">
          <h2>Connect</h2>

          <div className="profile-socials">
            {musician.instagram && (
              <a
                href={musician.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="profile-social-link"
              >
                <Camera size={18} />
                Instagram
                <ExternalLink size={14} />
              </a>
            )}

            {musician.youtube && (
              <a
                href={musician.youtube}
                target="_blank"
                rel="noopener noreferrer"
                className="profile-social-link"
              >
                <Video size={18} />
                YouTube
                <ExternalLink size={14} />
              </a>
            )}

            {musician.website && (
              <a
                href={musician.website}
                target="_blank"
                rel="noopener noreferrer"
                className="profile-social-link"
              >
                <Globe size={18} />
                Website
                <ExternalLink size={14} />
              </a>
            )}

            {!musician.instagram &&
             !musician.youtube &&
             !musician.website && (
              <p className="profile-muted">
                No social links provided.
              </p>
            )}
          </div>
        </section>

      </section>
    </main>
  );
}

export default Profile;
