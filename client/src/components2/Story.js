import {useState} from "react";
import { Button } from "antd";

const Story = (props) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const showModal = () => {
        setIsModalOpen(true);
        props.setTitle(`Projects / Stories / Items`)
        props.setLevel(2)
    };

    return <>
        <Button type="primary" onClick={showModal}>
            Create Story
        </Button>
    </>
}

export default Story;