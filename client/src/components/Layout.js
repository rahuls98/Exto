import {useState} from "react"
import { Layout } from "antd";
import SidebarMenu from "./SidebarMenu";
import MainContent from "./MainContent";
import ProjectsApp from "./ProjectsApp";
const { Footer, Sider, Content } = Layout;

const MainLayout = () => {
    const [content, setContent] = useState("Sprints")

    const setLayoutContent = (inp) => {
        setContent(inp);
    }

    return (content === "Sprints") ? <Layout style={{height: '100vh'}}>
        <Sider
            breakpoint="xl"
            collapsedWidth="0"
            onBreakpoint={(broken) => {
            console.log(broken);
            }}
            onCollapse={(collapsed, type) => {
            console.log(collapsed, type);
            }}
        >
            <div style={{height: "30px"}}></div>
            <SidebarMenu setLayoutContent={setLayoutContent}/>
        </Sider>
        <Layout>
            <Content style={{ height: "100vh", background: 'white'}}>
                <MainContent content={content} />
            </Content>
            <Footer style={{textAlign: "center", background: 'white'}}>
                Exto ©2022
            </Footer>
        </Layout>
    </Layout> : <ProjectsApp setLayoutContent={setLayoutContent}/>
}

export default MainLayout;