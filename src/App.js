import React from 'react';
import EventList from './components/EventList';
import NavBar from './NavBar';
import { Routes, Route } from "react-router-dom";
import Details from "./details"
import "./style.css";

export default function App() {
  // const args = JSON.parse(document.getElementById('data').text);
  const args = {
    events: [
      { title: 'Meeting with Prof', date: '2021-11-11T12:00' },
      { title: 'Anniversary', date: '2021-11-09' },
      { title: "Mom's Birthday", date: '2021-11-10T12:00' },
      { title: 'Assignment Due', date: '2021-11-12T23:59' },
      { title: 'Test!', date: '2021-11-09T12:00' },
      { title: 'Go out with friends', date: '2021-11-20T18:00' },
      { title: 'My Birthday!', date: '2021-01-16' },
      { title: 'My Birthday next year!', date: '2021-11-25' },
      { title: 'Thanksgiving', date: '2022-01-16' },
    ],
  };

  return (
    <div>
      <NavBar />
      <EventList events={args.events} />
      <Routes>
        <Route path='/details' element={<Details />}></Route>
        {/* <Route path='/' element={<EventList />}></Route> */}
      </Routes>
    </div>
  )
};

