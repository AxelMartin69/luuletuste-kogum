import React from 'react';
import { useState, useEffect } from 'react';
import Poems from './Poems';

export default function App() {
    const [poems, setPoems] = useState([]);

    useEffect(() => {
        fetchAllPoems();
    }, []);

    function fetchAllPoems() {
        fetch('http://localhost:8000/')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setPoems(data);
            });
    }

    return (
        <div>
            {poems.map((poem) => (
                <Poems key={poem.id} title={poem.title} body={poem.body} author={poem.author} entry_time={poem.entry_time} likes={poem.likes} />
            ))}
        </div>
    );
}
