import React, { useEffect, useState } from "react";
import { Select, Space, Table, Tag } from "antd";
import { Button, DatePicker, Form, Input } from "antd";
import { Modal } from "antd";
import api from "../api";
const { Column } = Table;

function ItemComponent(props) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isUpdateOpen, setUpdateModal] = useState(false);
  const [projects, setProjects] = useState([]);
  const [stories, setStories] = useState([]);
  const [itemTypes, setItemTypes] = useState([]);
  const [itemStatuses, setItemStatuses] = useState([]);
  const [currItem, setCurrItem] = useState({});
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    console.log(props.parentID);
    api
      .get("/projects", {
        params: {
          user_username: window.localStorage.getItem('user_username'),
          user_password: window.localStorage.getItem('user_password'),
        },
      })
      .then((res) => {
        setProjects(res.data.projects);

        res.data.projects.forEach((element) => {
          api
            .get("/stories", {
              params: {
                user_username: window.localStorage.getItem('user_username'),
                user_password: window.localStorage.getItem('user_password'),
                project: element.id,
              },
            })
            .then((res) => {
              stories.push(...res.data.stories);
              setStories(stories);
            })
            .catch((err) => {
              console.log(err);
            });
        });
      })
      .catch((err) => {
        console.log(err);
      });

    api
      .get("/item_types")
      .then((res) => {
        setItemTypes(res.data.item_types);
      })
      .catch((err) => {
        console.log(err);
      });

    api
      .get("/item_statuses")
      .then((res) => {
        setItemStatuses(res.data.item_statuses);
      })
      .catch((err) => {
        console.log(err);
      });

    api
      .get("/employees", {
        params: {
          user_username: window.localStorage.getItem('user_username'),
          user_password: window.localStorage.getItem('user_password'),
        },
      })
      .then((res) => {
        setEmployees(res.data.employees);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const onUpdate = (values) => {
    console.log("Success", values);
    const updateBody = {};
    updateBody.user_username = window.localStorage.getItem('user_username');
    updateBody.user_password = window.localStorage.getItem('user_password');
    updateBody.item = currItem.id;
    updateBody.title = currItem.title;
    updateBody.description = currItem.description;
    updateBody.story = currItem.story;
    updateBody.status = values.status;
    updateBody.type = currItem.type;
    updateBody.sprint = (values.status === 1) ? null : currItem.sprint;
    values.assigned_to
      ? (updateBody.assigned_to = values.assigned_to)
      : (updateBody.assigned_to = null);

    api
      .put("/items", updateBody)
      .then((res) => {
        alert(res.data.message)
        props.setTable(2, props.parentID);
      })
      .catch((err) => {
        console.log(err);
        alert(err.response.data.message)
      });
    setCurrItem({});
    setUpdateModal(false);
  };
  {
    console.log("Props", props);
  }

  const onFinish = (values) => {
    const createBody = {};
    createBody.user_username = window.localStorage.getItem('user_username');
    createBody.user_password = window.localStorage.getItem('user_password');
    createBody.title = values.title;
    createBody.story = props.parentID;
    createBody.type = values.type;

    api
      .post("/items", createBody)
      .then((res) => {
        alert(res.data.message)
        props.setTable(2, props.parentID);
      })
      .catch((err) => {
        console.log(err);
        alert(err.response.data.message)
      });

    setIsModalOpen(false);
  };

  const deleteItem = (id) => {
    api
      .delete("/items", {
        data: {
          user_username: window.localStorage.getItem('user_username'),
          user_password: window.localStorage.getItem('user_password'),
          item: id,
        },
      })
      .then((res) => {
        alert(res.data.message)
        props.setTable(2, props.parentID);
      })
      .catch((err) => {
        console.log(err);
        alert(err.response.data.message)
      });
  };

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
    setUpdateModal(false);
    setCurrItem(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
    setUpdateModal(false);
    setCurrItem(false);
  };
  return (
    <div>
      <>
        <Button type="primary" onClick={showModal}>
          Create Item
        </Button>
        <Modal
          title="Create Item"
          open={isModalOpen}
          onOk={handleOk}
          onCancel={handleCancel}
          footer={[]}
        >
          <Form
            name="basic"
            labelCol={{
              span: 8,
            }}
            wrapperCol={{
              span: 16,
            }}
            initialValues={{
              remember: false,
            }}
            onFinish={onFinish}
            autoComplete="off"
          >
            <Form.Item
              label="Title"
              name="title"
              rules={[
                {
                  required: true,
                  message: "Required!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            {/* <Form.Item
              label="Story"
              name="story"
              rules={[
                {
                  required: true,
                  message: "Required!",
                },
              ]}
            >
              <Select
                options={
                  stories.find((story) => story.id === props.parentID)
                    ? [
                        {
                          value: stories.find(
                            (story) => story.id === props.parentID
                          ).id,
                          label: stories.find(
                            (story) => story.id === props.parentID
                          ).title,
                        },
                      ]
                    : []
                }
              />
            </Form.Item> */}
            <Form.Item
              label="Type"
              name="type"
              rules={[
                {
                  required: true,
                  message: "Required!",
                },
              ]}
            >
              <Select
                options={itemTypes.map((it) => {
                  const obj = {};
                  obj.value = it.id;
                  obj.label = it.title;
                  return obj;
                })}
              />
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
      </>
      <Modal
        title="Update Modal"
        open={isUpdateOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        footer={[]}
      >
        <Form
          name="Update"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          initialValues={{
            remember: false,
          }}
          onFinish={onUpdate}
          autoComplete="off"
        >
          {/* <Form.Item
            label="Title"
            name="title"
            rules={[
              {
                required: true,
                message: "Please enter title",
              },
            ]}
          >
            <Input
              defaultValue={
                props.data.find((item) => item.id === currItem.id)
                  ? props.data.find((item) => item.id === currItem.id).title
                  : null
              }
            />
          </Form.Item> */}

          {/* <Form.Item
            label="Description"
            name="description"
            rules={[
              {
                required: true,
                message: "Please enter description",
              },
            ]}
          >
            <Input
              defaultValue={
                props.data.find((item) => item.id === currItem.id)
                  ? props.data.find((item) => item.id === currItem.id)
                      .description
                  : null
              }
            />
          </Form.Item> */}

          {/* <Form.Item
            label="Story"
            name="story"
            rules={[
              {
                required: true,
                message: "Please enter story",
              },
            ]}
          >
            <Select
              options={
                stories.find((story) => story.id === props.parentID)
                  ? [
                      {
                        value: stories.find(
                          (story) => story.id === props.parentID
                        ).id,
                        label: stories.find(
                          (story) => story.id === props.parentID
                        ).title,
                      },
                    ]
                  : []
              }
            />
          </Form.Item> */}
          {/* <Form.Item
            label="Type"
            name="type"
            rules={[
              {
                required: true,
                message: "Please enter type",
              },
            ]}
          >
            <Select
              options={itemTypes.map((it) => {
                const obj = {};
                obj.value = it.id;
                obj.label = it.title;
                return obj;
              })}
            />
          </Form.Item> */}
          <Form.Item
            label="Status"
            name="status"
            rules={[
              {
                required: true,
                message: "Please enter status",
              },
            ]}
          >
            <Select
              options={itemStatuses.map((it) => {
                const obj = {};
                obj.value = it.id;
                obj.label = it.title;
                return obj;
              })}//.filter((it) => it.label !== "Backlog")}
            />
          </Form.Item>
          {currItem.sprint != null && (
            <Form.Item
              label="Assigned To"
              name="assigned_to"
              rules={[
                {
                  required: true,
                  message: "Please enter assigned_to",
                },
              ]}
            >
              <Select
                options={employees.map((emp) => {
                  const obj = {};
                  obj.value = emp.id;
                  obj.label = emp.email;
                  return obj;
                })}
              />
            </Form.Item>
          )}
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
      <Table dataSource={props.data} style={{ paddingTop: 25 }}>
        <Column
          title="Title"
          dataIndex="title"
          key="title"
        />
        <Column title="Assigned To" dataIndex="assigned_to" key="assigned_to" render={(_, record) =>
            record.assigned_to || "-"
          }/>
        <Column title="Sprint" dataIndex="sprint" key="sprint" render={(_, record) =>
            record.sprint || "-"
          }/>
        <Column
          title="Type"
          render={(_, record) =>
            itemTypes.find((types) => types.id === record.type)
              ? itemTypes.find((types) => types.id === record.type).title
              : record.type
          }
          key="type"
        />
        <Column
          title="Status"
          render={(_, record) =>
            itemStatuses.find((status) => status.id === record.status)
              ? itemStatuses.find((status) => status.id === record.status).title
              : record.type
          }
          key="status"
        />
        <Column
          title="Action"
          key="action"
          render={(_, record) => (
            <Space size="middle">
              <a
                onClick={() => {
                  setCurrItem(props.data.find((item) => item.id === record.id));
                  setUpdateModal(true);
                }}
              >
                Update{" "}
              </a>
              <a
                onClick={() => {
                  deleteItem(record.id);
                }}
              >
                Delete
              </a>
            </Space>
          )}
        />
      </Table>
    </div>
  );
}

export default ItemComponent;
