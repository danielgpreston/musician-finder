import { MapPin, CalendarDays, ExternalLink, Camera, Video } from "lucide-react";
import { mockMusicians } from "../data/mockMusicians";
import { useParams } from "react-router-dom";
import "./Profile.css";

function Profile() {
  const { id } = useParams();

  const musician = mockMusicians.find((musician) => musician.id === Number(id));

  if (!musician) {
    return (
      <main className="profile-page">
        <section className="profile-card">
          <h1>Musician not found.</h1>
          <p>This profile doesn't exist.</p>
        </section>
      </main>
    )
  }

  return (
    <main className="profile-page">
      <section className="profile-card">

        <header className="profile-header">
          <div className="profile-avatar">
            {musician.name.charAt(0)}
          </div>

          <div>
            <h1>{musician.name}</h1>

            <p className="profile-location">
              <MapPin size={16} />
              {musician.location}
            </p>
          </div>
        </header>

        <section className="profile-section">
          <h2>About</h2>
          <p>{musician.bio}</p>
        </section>

        <section className="profile-section">
          <h2>Instruments</h2>

          <div className="profile-tags">
            {musician.instruments.map((instrument) => (
              <span className="profile-tag" key={instrument}>
                {instrument}
              </span>
            ))}
          </div>
        </section>

        <section className="profile-section">
          <h2>Genres</h2>

          <div className="profile-tags">
            {musician.genres.map((genre) => (
              <span className="profile-tag" key={genre}>
                {genre}
              </span>
            ))}
          </div>
        </section>

        <section className="profile-section">
          <h2>Experience</h2>

          <div className="profile-experience">
            <CalendarDays size={18} />
            <span>
              {musician.experience}{" "}
              {musician.experience === 1 ? "year" : "years"} of experience
            </span>
          </div>
        </section>

        <section className="profile-section">
          <h2>Looking For</h2>

          {musician.lookingFor?.length > 0 ? (
            <div className="profile-tags">
              {musician.lookingFor.map((instrument) => (
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
            {musician.socials?.instagram && (
              <a
                href={musician.socials.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="profile-social-link"
              >
                <Camera size={18} />
                Instagram
                <ExternalLink size={14} />
              </a>
            )}

            {musician.socials?.youtube && (
              <a
                href={musician.socials.youtube}
                target="_blank"
                rel="noopener noreferrer"
                className="profile-social-link"
              >
                <Camera size={18} />
                YouTube
                <ExternalLink size={14} />
              </a>
            )}
          </div>
        </section>

      </section>
    </main>
  );
}

export default Profile;
