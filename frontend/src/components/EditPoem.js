import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

export default function EditPoem() {
    const params = useParams();
    const token = localStorage.getItem('token');
    const [poemTitle, setPoemTitle] = useState('');
    const [poemBody, setPoemBody] = useState('');

    const fetchPoemById = (poemId) => {
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };
        fetch(`http://127.0.0.1:8000/poems/${poemId}`, options)
            .then((response) => response.json())
            .then((response) => {
                setPoemTitle(response.title);
                setPoemBody(response.body);
            });
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const pTitle = event.target.form[0].value;
        const pBody = event.target.form[1].value;
        console.log(pTitle, pBody);

        const options = {
            method: 'PUT',
            url: `http://127.0.0.1:8000/poems/update/${params.poemId}`,
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            data: { title: pTitle, body: pBody },
        };

        axios
            .request(options)
            .then(function (response) {
                console.log(response.data);
            })
            .catch(function (error) {
                console.error(error);
            });
    };

    useEffect(() => {
        fetchPoemById(params.poemId);
    }, []);

    return (
        <div>
            <h1>Poem title is {poemTitle}</h1>
            <form>
                <label>
                    Title:
                    <input value={poemTitle} onChange={(e) => setPoemTitle(e.target.value)} />
                </label>
                <label>
                    Poem:
                    <textarea value={poemBody} onChange={(e) => setPoemBody(e.target.value)} />
                </label>
                <button type="submit" id={params.poemId} onClick={(e) => handleSubmit(e)}>
                    Submit
                </button>
            </form>
        </div>
    );
}
