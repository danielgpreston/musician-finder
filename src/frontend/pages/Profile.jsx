import { MapPin } from "lucide-react";
import { mockMusicians } from "../data/mockMusicians";
import "./Profile.css";

function Profile() {
  const musician = mockMusicians[0];

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
      </section>
    </main>
  );
}

export default Profile;