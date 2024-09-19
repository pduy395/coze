export class Chatbot {
  constructor(name, description, prompt, llm_name, update_time, favourite) {
    this.name = name;
    this.description = description;
    this.prompt = prompt;
    this.llm_name = llm_name;
    this.update_time = update_time;
    this.favourite = favourite;
  }
}