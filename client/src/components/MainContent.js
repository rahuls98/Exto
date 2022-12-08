import SprintContent from "./SprintsContent"

const MainContent = (props) => {
    const getContent = () => {
        switch (props.content) {
            case "Sprints": return <SprintContent />
            case "Projects": return <h1>Projects content</h1>
        }
    }

    return <div style={{ padding: 24, minHeight: "360", background: "white" }}>
        {getContent()}    
    </div>
}

export default MainContent;