import { useState } from "react";
import { ShieldCheck, Search, Users } from "lucide-react";
import "./Admin.css";

function Admin() {
    const [search, setSearch] = useState("");

    // example users
    const [users, setUsers] = useState([
        {
            id: 1,
            username: "GuitarPlayer",
            email: "guitar@band.com",
            active: true
        },
        {
            id: 2,
            username: "Drummer",
            email: "drummer@band.com",
            active: true
        },
        {
            id: 3,
            username: "BassPlayer",
            email: "bass@band.com",
            active: false
        }
    ]);

    const filteredUsers = users.filter((user) =>
        user.username.toLowerCase().includes(search.toLowerCase()) ||
        user.email.toLowerCase().includes(search.toLowerCase())
    );


    const activeUsers = users.filter((user) => user.active).length;

    function toggleUserStatus(id) {
        setUsers((previousUsers) =>
            previousUsers.map((user) =>
                user.id === id
                    ? { ...user, active: !user.active }
                    : user
            )
        );
    }

    return (
        <div className="admin-page">

            <div className="admin-header">
                <ShieldCheck size={32} />
                <div>
                    <h1>Admin Tools</h1>
                    <p>Manage users and musician profiles</p>
                </div>
            </div>

            <div className="admin-stats">

                <div className="admin-stat-card">
                    <h3>Total Users</h3>
                    <p>{users.length}</p>
                </div>

                <div className="admin-stat-card">
                    <h3>Active Users</h3>
                    <p>{activeUsers}</p>
                </div>

                <div className="admin-stat-card">
                    <h3>Inactive Users</h3>
                    <p>{users.length - activeUsers}</p>
                </div>

            </div>

            <div className="admin-user-management">

                <h2>
                    <Users size={24} /> User Management
                </h2>

                <div className="admin-search">
                    <Search size={20} />
                    <input
                        type="text"
                        aria-label="Search users"
                        placeholder="Search by username or email..."
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                    />
                </div>

                <div className="admin-user-list">

                    {filteredUsers.length === 0 && (
                        <p>No users found.</p>
                    )}

                    {filteredUsers.map((user) => (
                        <div className="admin-user-card" key={user.id}>

                            <div className="admin-user-info">
                                <h3>{user.username}</h3>
                                <p>{user.email}</p>

                                <span
                                    className={
                                        user.active
                                            ? "admin-status-active"
                                            : "admin-status-inactive"
                                    }
                                >
                                    {user.active ? "Active" : "Inactive"}
                                </span>
                            </div>

                            <button
                                type="button"
                                className={
                                    user.active
                                        ? "admin-deactivate-button"
                                        : "admin-activate-button"
                                }
                                onClick={() => toggleUserStatus(user.id)}
                            >
                                {user.active ? "Deactivate" : "Activate"}
                            </button>

                        </div>
                    ))}

                </div>
            </div>
        </div>
    );
}

export default Admin;