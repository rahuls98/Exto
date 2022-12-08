import {Menu} from 'antd';

const SidebarMenu = (props) => {
    return <Menu
        theme="dark"
        mode="inline"
        defaultSelectedKeys={["1"]}
        items={[
            "Sprints",
            "Projects"
        ].map((label, index) => ({
            key: String(index + 1),
            label: label,
            onClick: () => props.setLayoutContent(label)
        }))}
    >
    </Menu>
}

export default SidebarMenu;