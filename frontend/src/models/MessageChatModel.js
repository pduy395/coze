export class MessageChat {
  constructor(answer, input_tokens, output_tokens, time, question, latency) {
    this.answer = answer;
    this.input_tokens = input_tokens;
    this.output_tokens = output_tokens;
    this.time = time;
    this.question = question;
    this.latency = latency;
  }
}