import "../App.css";
import ContentComponent from "./ContentComponent";
import React, { useEffect, useState } from "react";
import { Layout, Menu } from "antd";
import { Typography } from "antd";
import api from "../api";

const { Title } = Typography;
const { Content, Footer, Sider } = Layout;

const ProjectsApp = (props) => {
  const [bc, setBc] = useState("Projects");
  const [level, setLevel] = useState(0); // 0 is Project Level
  const [tab, setTab] = useState("Projects");
  const [parentID, setParentID] = useState(null);
  const [tableData, setData] = useState([]);

  useEffect(() => {
    api
    .get("/projects", {
      params: {
        user_username: "user@nike.com",
        user_password: "user@nike.com",
      },
    })
    .then(function (response) {
      setData(response.data.projects);
    })
    .catch(function (error) {
      console.log(error);
    });
  }, []);

  const setTable = (level, id) => {
    setParentID(id);
    switch (level) {
      case 0:
        api
          .get("/projects", {
            params: {
              user_username: "user@nike.com",
              user_password: "user@nike.com",
            },
          })
          .then(function (response) {
            console.log(response.data.projects)
            setData(response.data.projects);
          })
          .catch(function (error) {
            console.log(error);
          });
        setBc("Projects");
        setLevel(0);
        break;
      case 1:
        //stories
        api
          .get("/stories", {
            params: {
              user_username: "user@nike.com",
              user_password: "user@nike.com",
              project: id,
            },
          })
          .then(function (response) {
            console.log(response.data.stories)
            setData(response.data.stories);
          })
          .catch(function (error) {
            console.log(error);
          });
        setBc("Projects / Stories");
        setLevel(1);
        break;
      case 2:
        //items
        api
          .get("/items", {
            params: {
              user_username: "user@nike.com",
              user_password: "user@nike.com",
              story: id,
            },
          })
          .then(function (response) {
            setData(response.data.items);
          })
          .catch(function (error) {
            console.log(error);
          });
        setBc("Projects / Stories / Items");
        setLevel(2);
        break;
      default:
        //default to projects
        setData([
          {
            key: "1",
            firstName: "John",
            lastName: "Brown",
            age: 32,
            address: "New York No. 1 Lake Park",
            tags: ["nice", "developer"],
          },
          {
            key: "2",
            firstName: "Jim",
            lastName: "Green",
            age: 42,
            address: "London No. 1 Lake Park",
            tags: ["loser"],
          },
          {
            key: "3",
            firstName: "Joe",
            lastName: "Black",
            age: 32,
            address: "Sidney No. 1 Lake Park",
            tags: ["cool", "teacher"],
          },
        ]);
        break;
    }
  };

  return (
    <Layout style={{height: '100vh'}}>
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
        <Menu
            theme="dark"
            mode="inline"
            defaultSelectedKeys={["2"]}
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
      </Sider>
      <Layout>
            <Content style={{ height: "100vh", background: 'white'}}>
                <ContentComponent level={level} data={tableData} setTable={setTable} parentID={parentID} bc={bc} />
            </Content>
        <Footer
          style={{
            textAlign: "center",
          }}
        >
          Exto ©2022
        </Footer>
      </Layout>
    </Layout>
  );
};
export default ProjectsApp;
