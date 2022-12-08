import {useState} from 'react'
import "./App.css";
import Layout from './components/Layout';

const App = () => {
	const [content, setContent] = useState("Sprints")

	const setMainContent = () => {
		switch (content) {
			case "Sprints":
				return <h1>Sprints</h1>
			case "Projects":
				return <h1>Projects</h1>
		}
	}

	return <div><Layout /></div>
};

export default App;
