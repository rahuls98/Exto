import {useState, useEffect} from "react";
import { Button, DatePicker, Form, Input, Modal } from "antd";
import { Select } from "antd";
import { Space, Table, Tag } from "antd";
import api from "../api";
const { Column } = Table;

const Project = (props) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [projects, setProjects] = useState([])
    const [projectManagers, setProjectManagers] = useState([]);
    const [scrumMaster, setScrumMasters] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [projectManagerList, setPM] = useState([]);
    const [scrumMasterList, setSM] = useState([]);
    const [customerList, setCustomerList] = useState([]);
    const [currProject, setCurrProject] = useState({});
    const [modelOperation, setModalOperation] = useState("Create");

    useEffect(() => {
        api.get("/projects", {
            params: {
                user_username: "user@nike.com",
                user_password: "user@nike.com",
            },
        }).then(function (response) {
            setProjects(response.data.projects);
        }).catch(function (error) {
            console.log(error);
        });

        api
        .get("/project_managers", {
        params: {
            user_username: "user@nike.com",
            user_password: "user@nike.com",
        },
        })
        .then(function (response) {
        setPM(response.data.project_managers);
        const pmOption = response.data.project_managers.map((item) => {
            const object = {};
            object.value = item.id;
            object.label = item.first_name + item.last_name;
            return object;
        });
        setProjectManagers(pmOption);
        })
        .catch(function (error) {
        console.log(error);
        });

        api
        .get("/scrum_masters", {
        params: {
            user_username: "user@nike.com",
            user_password: "user@nike.com",
        },
        })
        .then(function (response) {
        setSM(response.data.scrum_masters);
        const scrumOption = response.data.scrum_masters.map((item) => {
            const object = {};
            object.value = item.id;
            object.label = item.first_name + item.last_name;
            return object;
        });
        setScrumMasters(scrumOption);
        })
        .catch(function (error) {
        console.log(error);
        });

        api
        .get("/customers", {
        params: {
            user_username: "user@nike.com",
            user_password: "user@nike.com",
        },
        })
        .then(function (response) {
        setCustomerList(response.data.customers);
        const customerOption = response.data.customers.map((item) => {
            const object = {};
            object.value = item.id;
            object.label = item.name;
            return object;
        });
        setCustomers(customerOption);
        })
        .catch(function (error) {
        console.log(error);
        });
    }, [])

    const parseDate = (strDate) => {
        return new Date(strDate).toDateString();
    };

    const getProject = (id) => {
        return props.data.find((item) => item.id === id);
      };
    
      const deleteProject = (id) => {
        const delBody = {};
        delBody.user_username = "user@nike.com";
        delBody.user_password = "user@nike.com";
        delBody.project = id;
    
        api
          .delete("/projects", { data: delBody })
          .then((res) => {
            props.setTable(0, null);
          })
          .catch((err) => {
            console.log(err);
          });
      };
    

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
      };
    
    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const onFinish = (values) => {
        if (modelOperation == "Create") {
          const project = {};
          project.user_username = "user@nike.com";
          project.user_password = "user@nike.com";
          project.title = values.title;
          project.customer = values.customer;
          project.start_date = `${values.startDate.year()}-${
            values.startDate.month() + 1
          }-${values.startDate.date().toString().padStart(2, "0")}`;
          project.end_date = `${values.endDate.year()}-${
            values.endDate.month() + 1
          }-${values.endDate.date().toString().padStart(2, "0")}`;
          project.project_manager = values.projectManager;
          project.scrum_master = values.scrumMaster;
          console.log("Success:", values);
          api
            .post("/projects", project)
            .then(function (res) {
              props.setTable(0, null);
            })
            .catch(function (err) {
              console.log(err);
            });
        } else {
          const project = {};
          project.user_username = "user@nike.com";
          project.user_password = "user@nike.com";
          project.title = values.title;
          project.project = currProject.id;
          project.customer = values.customer;
          project.start_date = `${values.startDate.year()}-${
            values.startDate.month() + 1
          }-${values.startDate.date().toString().padStart(2, "0")}`;
          project.end_date = `${values.endDate.year()}-${
            values.endDate.month() + 1
          }-${values.endDate.date().toString().padStart(2, "0")}`;
          project.project_manager = values.projectManager;
          project.scrum_master = values.scrumMaster;
          api
            .put("/projects", project)
            .then(function (res) {
              props.setTable(0, null);
            })
            .catch(function (err) {
              console.log(err);
            });
        }
        setIsModalOpen(false);
      };
      const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
      };

    return <>
        <Button type="primary" onClick={showModal}>
            Create Project
        </Button>
        <Modal
          title="Basic Modal"
          open={isModalOpen}
          onOk={handleOk}
          onCancel={handleCancel}
        >
        <Form
            name="basic"
            labelCol={{
                span: 8,
            }}
            wrapperCol={{
                span: 16,
            }}
            default={{
                remember: false,
            }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            >
            <Form.Item
                label="Title"
                name="title"
                rules={[
                {
                    required: true,
                    message: "Please enter title",
                },
                ]}
            >
                {console.log("model operation", modelOperation)}
                {console.log(currProject.title)}
                <Input
                // defaultValue={modelOperation === "Update" ? currProject.title : null}
                />
            </Form.Item>
            <Form.Item
                label="Customer"
                name="customer"
                rules={[
                {
                    required: true,
                    message: "Please enter customer",
                },
                ]}
            >
                {console.log("model operation", modelOperation)}
                {console.log("customer", currProject.customer)}
                <Select
                // defaultValue={
                //   modelOperation === "Update"
                //     ? customerList.find(
                //         (item) => item.id === currProject.customer
                //       ).name
                //     : null
                // }
                options={customers}
                />
            </Form.Item>

            <Form.Item
                label="Start Date"
                name="startDate"
                rules={[
                {
                    required: true,
                    message: "Please enter start date",
                },
                ]}
            >
                <DatePicker />
            </Form.Item>

            <Form.Item
                label="End Date"
                name="endDate"
                rules={[
                {
                    required: true,
                    message: "Please enter end date",
                },
                ]}
            >
                <DatePicker />
            </Form.Item>
            <Form.Item
                label="Project Manager"
                name="projectManager"
                rules={[
                {
                    required: true,
                    message: "Please enter project manager",
                },
                ]}
            >
                <Select
                // defaultValue={currProject.project_manager}
                options={projectManagers}
                />
            </Form.Item>

            <Form.Item
                label="Scrum Master"
                name="scrumMaster"
                rules={[
                {
                    required: true,
                    message: "Please enter scrum master",
                },
                ]}
            >
                <Select
                // defaultValue={currProject.scrum_master}
                options={scrumMaster}
                />
            </Form.Item>

            <Form.Item
                wrapperCol={{
                offset: 8,
                span: 16,
                }}
            >
                <Button type="primary" htmlType="submit">
                {modelOperation}
                </Button>
            </Form.Item>
            </Form>
        </Modal>
        <Table dataSource={projects} style={{ padding: 15 }}>
        <Column
            title="Title"
            render={(_, record) => (
                <a onClick={() => {
                    props.setTitle(`${record.title} / Stories`)
                    props.setLevel(2)
                }}>{record.title}</a>
            )}
            key="title"
        />
        <Column
            title="Project Manager"
            dataIndex="project_manager"
            key="project_manager"
        />
        <Column
            title="Scrum Master"
            dataIndex="scrum_master"
            key="scrum_master"
        />
        <Column
            title="Start Date"
            render={(_, record) => parseDate(record.start_date)}
            key="start_date"
        />
        <Column
            title="End Date"
            render={(_, record) => parseDate(record.start_date)}
            key="end_date"
        />
        <Column
            title="Action"
            key="action"
            render={(_, record) => (
            <Space size="middle">
                <a
                onClick={() => {
                    setCurrProject(getProject(record.id));
                    setModalOperation("Update");
                    showModal();
                }}
                >
                Update
                </a>
                <a
                onClick={() => {
                    deleteProject(record.id);
                }}
                >
                Delete
                </a>
            </Space>
            )}
        />
        </Table>
    </>
}

export default Project;