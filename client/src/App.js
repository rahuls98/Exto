// import {useState} from 'react'
// import "./App.css";
import Layout from './components/Layout';

import React, {useState, useEffect} from 'react';
import './index.css';
import { Form, Input, Button, Checkbox } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';

const App = () => {
	const [showLogin, setShowLogin] = useState(true)

	useEffect(() => {
		const user_username = window.localStorage.getItem('user_username')
		const user_password = window.localStorage.getItem('user_password')
		if (user_username || user_password) {
			setShowLogin(false)
		}
	}, [])

	const onFinish = values => {
		window.localStorage.setItem('user_username', values.user_username)
		window.localStorage.setItem('user_password', values.user_password)
		setShowLogin(false)
	};
	
	{
		return (showLogin) ? 
		<div style={{display: "flex", justifyContent: "center", paddingTop: "100px"}}>
		<Form
		  name="normal_login"
		  className="login-form"
		  initialValues={{
			remember: true,
		  }}
		  onFinish={onFinish}
		>
		  <Form.Item
			name="user_username"
			rules={[
			  {
				required: true,
				message: 'Please input your Username!',
			  },
			]}
		  >
			<Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
		  </Form.Item>
		  <Form.Item
			name="user_password"
			rules={[
			  {
				required: true,
				message: 'Please input your Password!',
			  },
			]}
		  >
			<Input
			  prefix={<LockOutlined className="site-form-item-icon" />}
			  type="password"
			  placeholder="Password"
			/>
		  </Form.Item>
	
		  <Form.Item>
			<Button type="primary" htmlType="submit" className="login-form-button">
			  Log in
			</Button>
		  </Form.Item>
		</Form>
		</div> : <Layout />
	}
};

export default App;
