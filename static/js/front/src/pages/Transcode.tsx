import React, {useEffect, useState} from "react";
import {useContext} from "react";
import SocketContext from "../contexts/socketContext";
import FileType from "../types/fileType";
import {Button, Checkbox, FormControl, InputLabel, LinearProgress, MenuItem, Select, Slider} from "@mui/material";

function Transcode(){
    const socket = useContext(SocketContext)

    const [files, setFiles] = useState<FileType[]>([])
    const [output, setOutput] = useState<FileType | null>(null)

    const [destinations, setDestinations] = useState<string[]>([])
    const [encoders, setEncoders] = useState<string[]>([])
    const [encoderPresets, setEncoderPresets] = useState<string[]>([])
    const [encoderTunes, setEncoderTunes] = useState<string[]>([])
    const [encoderProfiles, setEncoderProfiles] = useState<string[]>([])
    const [encoderLevels, setEncoderLevels] = useState<string[]>([])

    const [selectedFile, setSelectedFile] = useState<string | null>(null)
    const [destination, setDestination] = useState<string>("")
    const [encoder, setEncoder] = useState<string>("")
    const [encoderPreset, setEncoderPreset] = useState<string>("")
    const [encoderTune, setEncoderTune] = useState<string>("")
    const [encoderProfile, setEncoderProfile] = useState<string>("")
    const [encoderLevel, setEncoderLevel] = useState<string>("")
    const [quality, setQuality] = useState<number>(22)

    const [state, setState] = useState<"normal" | "preparing" | "running">("normal")
    const [progress, setProgress] = useState(0)
    const [speed, setSpeed] = useState(0)
    const [eta, setEta] = useState("")

    useEffect(() => {
        socket.on("files", setFiles)
        socket.on("output", setOutput)
        socket.on("state", setState)
        socket.on("progress", (progress: {progress: number, speed: number, eta: string}) => {
            if(state !== "running") setState("running")
            setProgress(progress.progress)
            setSpeed(progress.speed)
            setEta(progress.eta)
        })

        socket.emitWithAck("info").then(setFiles)
        socket.emitWithAck("output").then(setOutput)

        socket.emitWithAck("destinations").then(setDestinations)
        socket.emitWithAck("encoders").then(setEncoders)

        return () => {
            socket.off("info")
            socket.off("output")
            socket.off("state")
            socket.off("progress")
        }
    }, []);
    useEffect(() => {
        if(encoder === "" || !encoders.includes(encoder)) return;
        socket.emitWithAck("encoder_presets", encoder).then(setEncoderPresets)
        socket.emitWithAck("encoder_tunes", encoder).then(setEncoderTunes)
        socket.emitWithAck("encoder_profiles", encoder).then(setEncoderProfiles)
        socket.emitWithAck("encoder_levels", encoder).then(setEncoderLevels)
    }, [encoder]);

    function deleteFile(uuid: string){
        socket.emit("delete", uuid)
    }
    function startTranscode(){
        socket.emit("convert", {
            uuid: selectedFile,
            destination,
            encoder,
            encoderPreset,
            encoderTune,
            encoderProfile,
            encoderLevel,
            quality
        })
        setProgress(0)
    }

    return (
        <div className="container-fluid mt-3">
            <div className="row m-0">
                <div className="col-lg-6 col-12">
                    <h5>Files on server</h5>
                    {files.length === 0 && "None" }
                    <ul>
                        {files.map((file: any) => (
                            <li key={file.uuid}>
                                {file.name}
                                <Checkbox
                                    checked={selectedFile === file.uuid}
                                    onChange={() => setSelectedFile(file.uuid)}
                                />
                                <Button size="small" variant="text" color="error" onClick={() => deleteFile(file.uuid)}>
                                    <i className="material-icons">delete</i>
                                </Button>
                            </li>
                        ))}
                    </ul>
                    <Button variant="contained" color="error" onClick={() => deleteFile("all")}
                        hidden={files.length === 0}
                    >
                        Delete All
                    </Button>
                </div>
                <div className="col-lg-6 col-12 mt-5 mt-lg-0">
                    <h5>Output file</h5>
                    <span>{output ? output.name : "None"}</span><br/>
                    <a href="#" hidden={!output} onClick={e => {
                        e.preventDefault()
                        deleteFile("output")
                        setOutput(null)
                    }}>Delete</a>
                </div>

                {state !== "normal" ? (
                    <div className="col-12 mt-5">
                        <h5>Progress</h5>
                        {state === "preparing" ? "Preparing..." : (
                            <>
                                <p>Speed: {speed} fps</p>
                                <p>ETA: {eta}</p>
                            </>
                        )}
                        <LinearProgress variant={state === "preparing" ? "indeterminate" : "determinate"} value={progress} />
                    </div>
                ) : (
                    <>
                        <div
                            className="col-12 mt-5"
                            hidden={files.length === 0 || destinations.length === 0 || encoders.length === 0}
                        >
                            <h5>Output Options</h5>
                            <FormControl variant="standard" error={destination === ""} style={{width: 200}}>
                                <InputLabel>Destination</InputLabel>
                                <Select value={destination} onChange={e => setDestination(e.target.value as string)}>
                                    {destinations.map((destination: string) => (
                                        <MenuItem key={destination} value={destination}>{destination}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <FormControl variant="standard" error={encoder === ""} style={{width: 200}}>
                                <InputLabel>Encoder</InputLabel>
                                <Select value={encoder} onChange={e => setEncoder(e.target.value as string)}>
                                    {encoders.map((encoder: string) => (
                                        <MenuItem key={encoder} value={encoder}>{encoder}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </div>
                        <div
                            className="col-12 mt-5"
                            hidden={files.length === 0 || destination === "" || encoder === ""}
                        >
                            <h5>Encoder Options</h5>
                            <div className="w-100 d-flex justify-content-evenly">
                                <FormControl
                                    variant="standard"
                                    disabled={encoderPresets.length === 0}
                                    error={encoderPresets.length !== 0 && (encoderPreset === "" || !encoderPresets.includes(encoderPreset))}
                                    fullWidth
                                >
                                    <InputLabel>Encoder Presets</InputLabel>
                                    <Select value={encoderPreset} onChange={e => setEncoderPreset(e.target.value as string)}>
                                        {encoderPresets.map((encoderPreset: string) => (
                                            <MenuItem key={encoderPreset} value={encoderPreset}>{encoderPreset}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl
                                    variant="standard"
                                    disabled={encoderTunes.length === 0}
                                    error={encoderTunes.length !== 0 && (encoderTune === "" || !encoderTunes.includes(encoderTune))}
                                    fullWidth
                                >
                                    <InputLabel>Encoder Tunes</InputLabel>
                                    <Select value={encoderTune} onChange={e => setEncoderTune(e.target.value as string)}>
                                        {encoderTunes.map((encoderTune: string) => (
                                            <MenuItem key={encoderTune} value={encoderTune}>{encoderTune}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl
                                    variant="standard"
                                    disabled={encoderProfiles.length === 0}
                                    error={encoderProfiles.length !== 0 && (encoderProfile === "" || !encoderProfiles.includes(encoderProfile))}
                                    fullWidth
                                >
                                    <InputLabel>Encoder Profiles</InputLabel>
                                    <Select value={encoderProfile} onChange={e => setEncoderProfile(e.target.value as string)}>
                                        {encoderProfiles.map((encoderProfile: string) => (
                                            <MenuItem key={encoderProfile} value={encoderProfile}>{encoderProfile}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl
                                    variant="standard"
                                    disabled={encoderLevels.length === 0}
                                    error={encoderLevels.length !== 0 && (encoderLevel === "" || !encoderLevels.includes(encoderLevel))}
                                    fullWidth
                                >
                                    <InputLabel>Encoder Levels</InputLabel>
                                    <Select value={encoderLevel} onChange={e => setEncoderLevel(e.target.value as string)}>
                                        {encoderLevels.map((encoderLevel: string) => (
                                            <MenuItem key={encoderLevel} value={encoderLevel}>{encoderLevel}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </div>
                        </div>
                        <div
                            className="col-12 mt-5"
                            hidden={files.length === 0 || destination === "" || encoder === ""}
                        >
                            <h5>Quality: {quality} {quality === 0 && "(lossles)"}</h5>
                            <Slider
                                min={-51}
                                max={0}
                                value={-quality}
                                step={1}
                                marks
                                valueLabelFormat={(v) => `${-v}`}
                                onChange={(e, v) => setQuality(-(v as number))}
                                valueLabelDisplay="auto"
                            />
                        </div>
                        <Button
                            className="mt-5"
                            variant="contained"
                            color="success"
                            disabled={
                                selectedFile === null ||
                                files.length === 0 || destination === "" || encoder === "" ||
                                (encoderPresets.length !== 0 && (encoderPreset === "" || !encoderPresets.includes(encoderPreset))) ||
                                (encoderTunes.length !== 0 && (encoderTune === "" || !encoderTunes.includes(encoderTune))) ||
                                (encoderProfiles.length !== 0 && (encoderProfile === "" || !encoderProfiles.includes(encoderProfile))) ||
                                (encoderLevels.length !== 0 && (encoderLevel === "" || !encoderLevels.includes(encoderLevel)))
                            }
                            onClick={startTranscode}
                        >
                            Start Transcode
                        </Button>
                    </>
                )}
            </div>
        </div>
    )
}

export default Transcode;