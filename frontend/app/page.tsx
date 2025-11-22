"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { educationAPI, ChatResponse } from "@/lib/api-client"

interface Message {
  id: string
  type: "user" | "assistant"
  content: string
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
    }
    setMessages((prev) => [...prev, userMessage])
    const question = input
    setInput("")
    setIsLoading(true)
    setError(null)

    try {
      // Call backend API
      const response: ChatResponse = await educationAPI.chat({
        question: question,
        context: undefined,
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "assistant",
        content: response.answer,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to get response from server"
      setError(errorMsg)
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        type: "assistant",
        content: `Sorry, there was an error: ${errorMsg}. Please check that the backend is running.`,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border sticky top-0 bg-card z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Chat</h1>
            <p className="text-sm text-muted-foreground">Ask questions and get instant answers</p>
          </div>
          <Link href="/study-materials">
            <Button variant="outline">Study Materials</Button>
          </Link>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 text-destructive px-4 py-3 rounded-md max-w-4xl mx-auto mt-4 w-full">
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto max-w-4xl mx-auto w-full px-4 py-6">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-center">
            <Card className="p-8 max-w-md">
              <h2 className="text-xl font-semibold text-foreground mb-2">Welcome to AI Chat</h2>
              <p className="text-muted-foreground">
                Ask any question and get instant AI-powered answers to help with your studies.
              </p>
            </Card>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`mb-4 flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
            <Card
              className={`max-w-2xl px-4 py-3 ${
                message.type === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
            </Card>
          </div>
        ))}

        {isLoading && (
          <div className="mb-4 flex justify-start">
            <Card className="bg-muted text-foreground px-4 py-3">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce delay-200"></div>
              </div>
            </Card>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-border bg-card">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              type="text"
              placeholder="Ask a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
              className="flex-1"
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Sending..." : "Send"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
