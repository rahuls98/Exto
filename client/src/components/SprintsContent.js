import { useState, useEffect } from "react";
import { Typography, Modal, Button, Form, Input, InputNumber, DatePicker, Select, Transfer, Table, Space, Spin } from "antd";
import { Pie } from '@ant-design/plots';
import api from "../api";
import {CheckOutlined} from "@ant-design/icons"
const { Column } = Table;
const { Title } = Typography;


const SprintContent = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isMetricsModalOpen, setIsMetricsModalOpen] = useState(false);
    const [projects, setProjects] = useState([]);
    const [scrumMasters, setScrumMasters] = useState([]);
    const [targetKeys, setTargetKeys] = useState([]);
    const [selectedKeys, setSelectedKeys] = useState([]);
    const [sprints, setSprints] = useState([]);
    const [backlogItems, setBacklogItems] = useState([]);
    const [metricsConfig, setMetricsConfig] = useState({});
    
    useEffect(() => {
        api.get("/projects", {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
            },
        }).then(function (response) {
            const projectOptions = response.data.projects.map((item) => {
                const object = {};
                object.value = item.id;
                object.label = item.title;
                return object;
            });
            setProjects(projectOptions);
        }).catch(function (error) {
            console.log(error);
        });

        api.get("/sprints", {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
            },
        }).then(function (response) {
            console.log(response.data.sprints)
            setSprints(response.data.sprints);
        }).catch(function (error) {
            console.log(error);
        });

        api.get("/scrum_masters", {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
            },
        }).then(function (response) {
            const scrumMasterOptions = response.data.scrum_masters.map((item) => {
                const object = {};
                object.value = item.id;
                object.label = `${item.first_name} ${item.last_name}`
                return object;
            });
            setScrumMasters(scrumMasterOptions);
        }).catch(function (error) {
            console.log(error);
        });

        api.get("/items/backlog", {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
            },
        }).then(function (response) {
            const backlogItemOptions = response.data.backlog_items.map((item) => {
                const object = {};
                object.key = item.id;
                object.title = item.title;
                return object;
            })
            setBacklogItems(backlogItemOptions);
        }).catch(function (error) {
            console.log(error);
        });
    }, [])

    const showModal = () => {
        setIsModalOpen(true);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const handleMetricsModalCancel = () => {
        setIsMetricsModalOpen(false);
    }

    const getSprintMetrics = (sprint_id) => {
        setIsMetricsModalOpen(true);
        api.get(`/sprints/item_composition`, {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
                id: sprint_id
            },
        }).then(function (response) {
            const itemCompositions = response.data.item_compositions.map((item) => {
                const object = {};
                object.type = item.title;
                object.value = item.items;
                return object;
            });
            const config = {
                appendPadding: 10,
                data: itemCompositions,
                angleField: 'value',
                colorField: 'type',
                radius: 0.8,
                label: {
                    type: 'outer',
                    content: '{name} {percentage}',
                },
                interactions: [
                    {
                    type: 'pie-legend-active',
                    },
                    {
                    type: 'element-active',
                    },
                ],
            };
            setMetricsConfig(config);
        }).catch(function (error) {
            console.log(error);
        });
    }

    const onTransferChange = (nextTargetKeys, direction, moveKeys) => {
        setTargetKeys(nextTargetKeys);
      };
      const onTransferSelectChange = (sourceSelectedKeys, targetSelectedKeys) => {
        setSelectedKeys([...sourceSelectedKeys, ...targetSelectedKeys]);
      };
      const onTransferScroll = (direction, e) => {};

    const parseDate = (strDate) => {
        return new Date(strDate).toDateString();
    };

    const onFinish = async (values) => {
        const sprint = {};
        sprint.user_username = window.localStorage.getItem('user_username');
        sprint.user_password = window.localStorage.getItem('user_password');
        sprint.sprint_number = values.sprintNumber
        sprint.start_date = `${values.startDate.year()}-${values.startDate.month() + 1}-${values.startDate.date().toString().padStart(2, "0")}`
        sprint.duration = values.duration
        sprint.definition_of_done = values.definitionOfDone
        sprint.project = values.project
        sprint.scrum_master = values.scrumMaster
        sprint.items = values.items
        api
        .post("/sprints", sprint)
        .then(function (res) {
            console.log(res)
            alert(res.data.message);
            setIsModalOpen(false);
            window.location.reload(false);
        })
        .catch(function (err) {
            console.log(err);
            alert(err.response.data.message)
        });
    }

    const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
    };

    const markSprintComplete = (sprintId) => {
        const body = {};
        body.user_username = window.localStorage.getItem('user_username');
        body.user_password = window.localStorage.getItem('user_password');
        body.sprint = sprintId;
        api.put("/sprints/complete", body)
        .then(function (res) {
            console.log(res)
        })
        .catch(function (err) {
            console.log(err);
            alert(err)
        });

        api.get("/sprints", {
            params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
            },
        }).then(function (response) {
            console.log(response.data.sprints)
            window.location.reload(false);
        }).catch(function (error) {
            console.log(error);
        });
    }

    return <div>
        <Title style={{marginBottom: 20 }} level={2}>
            Sprints
        </Title>
        <Button type="primary" onClick={showModal}>
            Create Sprint
        </Button>
        <Modal
            title="Create Sprint"
            open={isModalOpen}
            onCancel={handleCancel}
            footer={[]}
            width={1000}
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
                    label="Sprint number"
                    name="sprintNumber"
                    rules={[
                        {
                        required: true,
                        message: "Please enter sprint number",
                        },
                    ]}
                >
                    <InputNumber min={1} max={100}/>
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
                    label="Duration (in weeks)"
                    name="duration"
                    rules={[
                        {
                        required: true,
                        message: "Please enter duration",
                        },
                    ]}
                >
                    <InputNumber min={1} max={4}/>
                </Form.Item>
                <Form.Item
                    label="Definition of done"
                    name="definitionOfDone"
                    rules={[]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                label="Project"
                name="project"
                rules={[
                    {
                    required: true,
                    message: "Please select project",
                    },
                ]}
                >
                    <Select options={projects} />
                </Form.Item>
                <Form.Item
                label="Scrum Master"
                name="scrumMaster"
                rules={[
                    {
                    required: true,
                    message: "Please select scrum_master",
                    },
                ]}
                >
                    <Select options={scrumMasters} />
                </Form.Item>
                <Form.Item
                    label="Select items"
                    name="items"
                    rules={[
                        {
                        required: true,
                        message: "Please select items",
                        },
                    ]}
                >
                    <Transfer
                        dataSource={backlogItems}
                        titles={['Backlog', 'Sprint']}
                        targetKeys={targetKeys}
                        selectedKeys={selectedKeys}
                        onChange={onTransferChange}
                        onSelectChange={onTransferSelectChange}
                        onScroll={onTransferScroll}
                        render={(item) => item.title}
                        showSelectAll={false}
                    />
                </Form.Item>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form>
        </Modal>
        <Modal
            title="Overview of sprint items"
            open={isMetricsModalOpen}
            onCancel={handleMetricsModalCancel}
            footer={[]}
            width={1000}
        >
            {
                (Object.keys(metricsConfig).length === 0) ? <Spin /> : <Pie {...metricsConfig} />
            }
        </Modal>
        <Table dataSource={sprints} style={{ paddingTop: 25 }}>
            <Column
                title="Sprint number"
                dataIndex="sprint_number"
                key="sprint_number"
            />
            <Column
                title="Project"
                dataIndex="project"
                key="project"
            />
            <Column
                title="Start date"
                render={(_, record) => parseDate(record.start_date)}
                dataIndex="start_date"
                key="start_date"
            />
            <Column
                title="Duration"
                render={(_, record) => `${record.duration} weeks`}
                dataIndex="duration"
                key="duration"
            />
            <Column
                title="Scrum master"
                dataIndex="scrum_master"
                key="scrum_master"
            />
            <Column
                title="Completed"
                dataIndex="completed"
                key="completed"
                render = {(_, record) => {
                    return (record.completed) ? <CheckOutlined style={{ fontSize: '16px', color: 'green' }} /> : null
                }}
            />
            <Column
                title="Actions"
                key="action"
                render={(_, record) => {
                        return (record.completed) ? null : 
                        <Space size="middle">
                            <a onClick={() => getSprintMetrics(record.id)}>Metrics</a>
                            <a onClick={() => markSprintComplete(record.id)}>Mark complete</a>
                        </Space>
                    }
                }
            />
        </Table>
    </div>
};

export default SprintContent;