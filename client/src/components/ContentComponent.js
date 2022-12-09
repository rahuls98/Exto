import React, { useState } from "react";
import { Content } from "antd/es/layout/layout";
import ProjectContent from "./ProjectContent";
import StoriesComponent from "./StroriesComponent";
import ItemComponent from "./ItemComponent";
// import StoriesComponent from "./xComponent";
import { Typography } from "antd";
const { Title } = Typography;

function ContentComponent(props) {
  const getComponentForLevel = (level) => {
    switch (level) {
      case 0:
        return <ProjectContent data={props.data} setTable={props.setTable} parentID = {props.parentID} />;
        break;
      case 1:
        return <StoriesComponent data={props.data} setTable={props.setTable} parentID = {props.parentID} />;
        break;
      case 2:
        return <ItemComponent data={props.data} setTable={props.setTable} parentID = {props.parentID} />;
        break;
      default:
        return null;
        break;
    }
  };
  return (
    <div style={{ padding: 24, minHeight: "360", background: "white" }}>
        <Title style={{marginBottom: 20 }} level={2}>
            {props.bc}
        </Title>
        {getComponentForLevel(props.level)}  
    </div>
  );
}

export default ContentComponent;
