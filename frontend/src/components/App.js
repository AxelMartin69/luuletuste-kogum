import { React, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Poems from './Poems';

export default function App() {
    const navigate = useNavigate();
    const [poems, setPoems] = useState([]);
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        fetchAllPoems();
    }, []);

    const fetchAllPoems = () => {
        fetch('http://127.0.0.1:8000/')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setPoems(data);
            });
    };

    const handleLogOut = () => {
        localStorage.removeItem('token');
        setToken(null);
    };

    return (
        <div>
            {!token ? (
                <div>
                    <button
                        onClick={() => {
                            navigate('/login');
                        }}>
                        Log In
                    </button>
                    {poems.map((poem) => (
                        <Poems key={poem.id} title={poem.title} body={poem.body} author={poem.author} entry_time={poem.entry_time} likes={poem.likes} />
                    ))}
                </div>
            ) : (
                <div>
                    <button
                        onClick={() => {
                            handleLogOut();
                        }}>
                        Log Out
                    </button>
                    <button onClick={navigate('/my-poems')}>My Poems</button>
                    {poems.map((poem) => (
                        <Poems key={poem.id} title={poem.title} body={poem.body} author={poem.author} entry_time={poem.entry_time} likes={poem.likes} token={token} />
                    ))}
                </div>
            )}
        </div>
    );
}
