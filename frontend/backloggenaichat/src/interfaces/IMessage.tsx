interface IMessage {
    sender: string,
    text: string,
    isAnswerLoading: boolean,
    isStreaming: boolean
}

export default IMessage