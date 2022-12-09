import {useState} from "react";
import { Button } from "antd";

const Item = (props) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const showModal = () => {
        setIsModalOpen(true);
    };

    return <>
        <Button type="primary" onClick={showModal}>
            Create Item
        </Button>
    </>
}

export default Item;