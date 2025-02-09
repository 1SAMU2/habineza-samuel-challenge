import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  inputText = '';
  outputText = '';
  isLoading = false;
  error = '';

  constructor(private http: HttpClient) {}

  async processText() {
    if (!this.inputText.trim()) {
      this.error = 'Please enter some text';
      return;
    }

    this.isLoading = true;
    this.error = '';

    try {
      const response: any = await this.http.post('https://your-backend-url.com/api/process', {
        text: this.inputText
      }).toPromise();

      this.outputText = response.response;
    } catch (err) {
      this.error = 'An error occurred while processing your request';
      console.error('Error:', err);
    } finally {
      this.isLoading = false;
    }
  }
}