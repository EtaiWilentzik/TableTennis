import './Video.css';
import {Nav} from "./NavBar";
const Video = () => {
    return (
        <>
        <video src="/video.mp4" className="video"  muted autoPlay  loop />
        </>
    );
}

export default Video;
