import { useState } from "react";
import { Typography } from "antd";
import Project from "./Project";
import Story from "./Story";
import Item from "./Item";
const { Title } = Typography;

const ProjectsContent = () => {
    const [title, setTitle] = useState("Projects")
    const [level, setLevel] = useState(0)

    const getContent = () => {
        switch(level) {
            case 0: return <Project setTitle={setTitle} setLevel={setLevel} />
            case 1: return <Story setTitle={setTitle} setLevel={setLevel} />
            case 2: return <Item setTitle={setTitle} setLevel={setLevel} />
        }
    }

    return <div>
        <Title style={{marginBottom: 20 }} level={2}>
            {title}
        </Title>
        {getContent()}
    </div>

}

export default ProjectsContent;