import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Poems from './Poems';

export default function MyPoems() {
    const navigate = useNavigate();
    const [poems, setPoems] = useState([]);
    const token = localStorage.getItem('token');

    useEffect(() => {
        fetchMyPoems(localStorage.getItem('token'));
    }, []);

    const fetchMyPoems = (token) => {
        const options = {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`,
            },
        };

        fetch('http://127.0.0.1:8000/users/me', options)
            .then((response) => response.json())
            .then((response) => {
                setPoems(response.poems);
            })
            .catch((err) => console.error(err));
    };

    return (
        <div>
            <button onClick={() => navigate('/new-poem')}>New Poem</button>
            {poems.map((poem) => (
                <div>
                    <Poems key={poem.id} title={poem.title} body={poem.body} author={poem.author} entry_time={poem.entry_time} likes={poem.likes} token={token} />
                    <button onClick={() => navigate(`/edit-poem/${poem.id}`)}>Edit Poem</button>
                </div>
            ))}
        </div>
    );
}
