import { useState, useEffect } from "react";
import { Button, Modal, Form, Input, Select, DatePicker, Table, Space } from "antd";
import api from "../api";
const { Column } = Table;

const Project = (props) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [customers, setCustomers] = useState([]);
    const [projectManagers, setProjectManagers] = useState([]);
    const [scrumMasters, setScrumMasters] = useState([]);
    const [projects, setProjects] = useState([]);

    useEffect(() => {
        api
        .get("/customers", {
        params: {
            user_username: "user@nike.com",
            user_password: "user@nike.com",
        },
        })
        .then(function (response) {
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

        api
        .get("/project_managers", {
        params: {
            user_username: "user@nike.com",
            user_password: "user@nike.com",
        },
        })
        .then(function (response) {
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

        api.get("/projects", {
            params: {
                user_username: "user@nike.com",
                user_password: "user@nike.com",
            },
        }).then(function (response) {
            const projectsRes = response.data.projects.map((eachProject) => {
                const ob = {...eachProject}
                api.get("/employees/full_name", {
                    params: {
                        user_username: "user@nike.com",
                        user_password: "user@nike.com",
                        employee: ob.project_manager
                    },
                }).then(res => {
                    ob.project_manager = res.data.full_name
                }).catch(err => {
                    console.log(err);
                })

                api.get("/employees/full_name", {
                    params: {
                        user_username: "user@nike.com",
                        user_password: "user@nike.com",
                        employee: ob.scrum_master
                    },
                }).then(res => {
                    ob.scrum_master = res.data.full_name
                }).catch(err => {
                    console.log(err);
                })
                return ob
            })
            console.log(projectsRes)
            setProjects(projectsRes);
        }).catch(function (error) {
            console.log(error);
        });
    }, [])

    const parseDate = (strDate) => {
        return new Date(strDate).toDateString();
    };

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const onFinish = (values) => {
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
            console.log(res)
        })
        .catch(function (err) {
            console.log(err);
        });
        setIsModalOpen(false);
    }

    const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
    };

    return <>
        <Button type="primary" onClick={showModal}>
            Create Project
        </Button>
        <Modal
            title="Create Project"
            open={isModalOpen}
            onCancel={handleCancel}
            footer={[]}
        >
            <Form
                name="basic"
                labelCol={{
                span: 8,
                }}
                wrapperCol={{
                span: 20,
                }}
                initialValues={{
                remember: true,
                }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                autoComplete="off"
            >
                <Form.Item
                    label="Title"
                    name="title"
                    rules={[
                        {
                            required: true,
                            message: "Please enter title",
                        },
                    ]}>
                    <Input />
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
                    <Select options={customers}/>
                </Form.Item>
                <Form.Item
                    label="Start Date"
                    name="startDate"
                    rules={[
                    {
                        required: true,
                        message: "Please enter start date",
                    },
                    ]}>
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
                    <Select options={projectManagers} />
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
                    <Select options={scrumMasters}/>
                </Form.Item>

                <Form.Item
                    wrapperCol={{
                    offset: 8,
                    span: 16,
                    }}
                >
                    <Button type="primary" htmlType="submit">
                    Submit
                    </Button>
                </Form.Item>
            </Form>
        </Modal>
        <Table dataSource={projects} style={{ paddingTop: 25 }}>
            <Column
                title="Title"
                dataIndex="title"
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
                render={(_, record) => parseDate(record.end_date)}
                key="end_date"
            />
            <Column
                title="Actions"
                key="actions"
                render={(_, record) => (
                <Space size="middle">
                    <a>Update</a>
                    <a>Delete</a>
                </Space>
                )}
            />
        </Table>
    </>
}

export default Project;
