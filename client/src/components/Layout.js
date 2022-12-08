import {useState} from "react"
import { Layout, Typography} from "antd";
import SidebarMenu from "./SidebarMenu";
import MainContent from "./MainContent";
const { Title } = Typography;
const { Header, Footer, Sider, Content } = Layout;

const MainLayout = () => {
    const [content, setContent] = useState("Sprints")

    const setLayoutContent = (inp) => {
        setContent(inp);
    }

    return <Layout style={{height: '100vh'}}>
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
            <div style={{height: "30px"}}>Exto</div>
            <SidebarMenu setLayoutContent={setLayoutContent}/>
        </Sider>
        <Layout>
            <Header style={{ padding: 0, background: "white" }}>
                <Title
                    style={{
                    marginLeft: 25,
                    marginBottom: 20,
                    }}
                    level={2}
                >
                    {content}
                </Title>
            </Header>
            <Content style={{ height: "100vh", background: 'white'}}>
                <MainContent content={content} />
            </Content>
            <Footer style={{textAlign: "center", background: 'white'}}>
                Exto ©2022
            </Footer>
        </Layout>
    </Layout>
}

export default MainLayout;