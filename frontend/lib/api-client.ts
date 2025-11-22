/**
 * API client for communicating with the backend
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

export class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string = BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      "Content-Type": "application/json",
    };

    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  public async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "GET" });
  }

  public async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  public async put<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  public async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }
}

// Create a singleton instance
export const apiClient = new APIClient();

// Education API types
export interface ChatRequest {
  question: string;
  context?: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
  context?: string;
}

export interface MCQ {
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
}

export interface ShortQuestion {
  question: string;
  expected_answer: string;
  difficulty: "easy" | "medium" | "hard";
}

export interface GenerateMaterialRequest {
  topic: string;
  level?: "beginner" | "intermediate" | "advanced";
  language?: string;
}

export interface GenerateMaterialResponse {
  topic: string;
  level: string;
  study_notes: string;
  story_explanation: string;
  summary: string;
  mcqs: MCQ[];
  short_questions: ShortQuestion[];
  image_url?: string;
}

// Education API methods
export const educationAPI = {
  chat: (request: ChatRequest): Promise<ChatResponse> =>
    apiClient.post<ChatResponse>("/api/education/chat", request),

  generateMaterial: (request: GenerateMaterialRequest): Promise<GenerateMaterialResponse> =>
    apiClient.post<GenerateMaterialResponse>("/api/education/generate-material", request),

  health: (): Promise<{ status: string; service: string; version: string }> =>
    apiClient.get("/api/v1/health"),
};
