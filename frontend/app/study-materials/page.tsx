"use client"

import type React from "react"
import { useState, useRef } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Skeleton } from "@/components/ui/skeleton"
import { educationAPI, GenerateMaterialResponse, MCQ, ShortQuestion } from "@/lib/api-client"

export default function StudyMaterialsPage() {
  const [topic, setTopic] = useState("")
  const [level, setLevel] = useState<"beginner" | "intermediate" | "advanced">("intermediate")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [material, setMaterial] = useState<GenerateMaterialResponse | null>(null)
  const materialsRef = useRef<HTMLDivElement>(null)

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topic.trim()) return

    setIsLoading(true)
    setError(null)
    setMaterial(null)

    try {
      const response = await educationAPI.generateMaterial({
        topic: topic,
        level: level,
        language: "english",
      })
      setMaterial(response)
      setTimeout(() => {
        materialsRef.current?.scrollIntoView({ behavior: "smooth" })
      }, 100)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Failed to generate materials"
      setError(errorMsg)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border sticky top-0 bg-card z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Study Materials</h1>
            <p className="text-sm text-muted-foreground">Generate comprehensive learning content</p>
          </div>
          <Link href="/">
            <Button variant="outline">Back to Chat</Button>
          </Link>
        </div>
      </header>

      {/* Generator Section */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card className="p-6 mb-8">
          <h2 className="text-xl font-semibold text-foreground mb-4">Generate Study Materials</h2>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Enter a topic (e.g., Photosynthesis, World War II)"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                disabled={isLoading}
                className="flex-1"
              />
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value as "beginner" | "intermediate" | "advanced")}
                disabled={isLoading}
                className="px-3 py-2 border border-input rounded-md bg-background text-foreground"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Generating..." : "Generate"}
              </Button>
            </div>
          </form>
        </Card>

        {/* Error Message */}
        {error && (
          <Card className="p-4 mb-8 border-destructive/20 bg-destructive/10">
            <p className="text-destructive font-medium">{error}</p>
          </Card>
        )}

        {/* Loading Skeleton */}
        {isLoading && (
          <div ref={materialsRef} className="space-y-6">
            <Card className="p-6">
              <Skeleton className="h-6 w-48 mb-4" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-3/4" />
            </Card>
            <Card className="p-6">
              <Skeleton className="h-6 w-32 mb-4" />
              <Skeleton className="h-40 w-full" />
            </Card>
          </div>
        )}

        {/* Study Materials */}
        {material && (
          <div ref={materialsRef} className="space-y-6">
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="notes">Notes</TabsTrigger>
                <TabsTrigger value="story">Story</TabsTrigger>
                <TabsTrigger value="mcq">MCQ</TabsTrigger>
                <TabsTrigger value="questions">Q&A</TabsTrigger>
              </TabsList>

              {/* Overview Tab */}
              <TabsContent value="overview" className="space-y-4">
                <Card className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-2">{material.topic}</h3>
                  <p className="text-sm text-muted-foreground mb-4">Level: {material.level}</p>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-foreground mb-2">Summary</h4>
                      <p className="text-foreground whitespace-pre-wrap">{material.summary}</p>
                    </div>
                    {material.image_url && (
                      <div>
                        <h4 className="font-medium text-foreground mb-2">Illustration</h4>
                        <img src={material.image_url} alt={material.topic} className="w-full rounded-lg" />
                      </div>
                    )}
                  </div>
                </Card>
              </TabsContent>

              {/* Notes Tab */}
              <TabsContent value="notes">
                <Card className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4">Study Notes</h3>
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <p className="whitespace-pre-wrap text-foreground">{material.study_notes}</p>
                  </div>
                </Card>
              </TabsContent>

              {/* Story Tab */}
              <TabsContent value="story">
                <Card className="p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4">Story-Based Explanation</h3>
                  <p className="whitespace-pre-wrap text-foreground">{material.story_explanation}</p>
                </Card>
              </TabsContent>

              {/* MCQ Tab */}
              <TabsContent value="mcq" className="space-y-4">
                <h3 className="text-lg font-semibold text-foreground">Multiple Choice Questions</h3>
                {material.mcqs.map((mcq: MCQ, index: number) => (
                  <Card key={index} className="p-6">
                    <h4 className="font-semibold text-foreground mb-3">
                      {index + 1}. {mcq.question}
                    </h4>
                    <div className="space-y-2 mb-4">
                      {mcq.options.map((option: string, optIndex: number) => (
                        <div
                          key={optIndex}
                          className={`p-3 rounded-lg border ${
                            option === mcq.correct_answer
                              ? "border-green-500/50 bg-green-500/10"
                              : "border-border bg-muted/50"
                          }`}
                        >
                          <p className="text-sm">
                            <span className="font-medium">{String.fromCharCode(65 + optIndex)}.</span> {option}
                          </p>
                        </div>
                      ))}
                    </div>
                    <details className="cursor-pointer">
                      <summary className="font-medium text-sm text-primary">Show Explanation</summary>
                      <p className="text-sm text-foreground mt-2">{mcq.explanation}</p>
                    </details>
                  </Card>
                ))}
              </TabsContent>

              {/* Questions Tab */}
              <TabsContent value="questions" className="space-y-4">
                <h3 className="text-lg font-semibold text-foreground">Short Answer Questions</h3>
                {material.short_questions.map((q: ShortQuestion, index: number) => (
                  <Card key={index} className="p-6">
                    <h4 className="font-semibold text-foreground mb-3">
                      {index + 1}. {q.question}
                    </h4>
                    <div className="mb-3">
                      <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-muted text-foreground capitalize">
                        {q.difficulty}
                      </span>
                    </div>
                    <details className="cursor-pointer">
                      <summary className="font-medium text-sm text-primary">Show Answer</summary>
                      <p className="text-sm text-foreground mt-2 whitespace-pre-wrap">{q.expected_answer}</p>
                    </details>
                  </Card>
                ))}
              </TabsContent>
            </Tabs>
          </div>
        )}

        {/* Empty State */}
        {!material && !isLoading && (
          <Card className="p-8 text-center">
            <h3 className="text-lg font-semibold text-foreground mb-2">No Materials Generated Yet</h3>
            <p className="text-muted-foreground">Enter a topic and click "Generate" to create study materials</p>
          </Card>
        )}
      </div>
    </div>
  )
}
