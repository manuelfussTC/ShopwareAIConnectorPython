<?php

class EmbeddingGenerator
{
    private $apiKey;
    private $model;
    private $maxRetries;
    private $retryDelay;

    public function __construct($apiKey, $model = "text-embedding-ada-002", $maxRetries = 3, $retryDelay = 5)
    {
        $this->apiKey = $apiKey;
        $this->model = $model;
        $this->maxRetries = $maxRetries;
        $this->retryDelay = $retryDelay;
    }

    public function generateEmbeddingsForAPIEndpoints($apiEndpoints)
    {
        $url = "https://api.openai.com/v1/embeddings";
        $headers = [
            "Content-Type: application/json",
            "Authorization: Bearer " . $this->apiKey
        ];

        $embeddings = [];

        foreach ($apiEndpoints as $path => $methods) {
            foreach ($methods as $httpMethod => $data) {
                $text = $this->extractRelevantInfo($data);
//                if (strpos($text, 'infoShopwareVersion') !== false) {
//                    echo "Word Found!\n";
//                    echo "Extracted text: $text\n";
//                }
//                continue;
                $data = json_encode(["input" => $text, "model" => $this->model]);

                $retryCount = 0;
                while ($retryCount <= $this->maxRetries) {
                    $ch = curl_init($url);
                    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
                    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

                    $result = curl_exec($ch);
                    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

                    if ($httpCode == 200) {
                        $decodedResult = json_decode($result, true);
                        if (isset($decodedResult['data']) && isset($decodedResult['data'][0]['embedding'])) {
                            $embeddings[$path][$httpMethod] = $decodedResult['data'][0]['embedding'];
                        }
                        break; // Break the loop on success
                    } else if ($httpCode == 503 && $retryCount < $this->maxRetries) {
                        sleep($this->retryDelay);
                        $retryCount++;
                        continue; // Retry on 503 error
                    } else {
                        // Handle other errors or max retry count reached
                        echo "HTTP Fehler: Statuscode " . $httpCode . "<br>";
                        echo "Antwort: " . $result . "<br>";
                        break;
                    }
                }
                curl_close($ch);
            }
        }

        return $embeddings;
    }

    public function generateEmbeddingForPrompt($prompt)
    {
        $url = "https://api.openai.com/v1/embeddings";
        $headers = [
            "Content-Type: application/json",
            "Authorization: Bearer " . $this->apiKey
        ];

        $data = json_encode(["input" => $prompt, "model" => $this->model]);

        $retryCount = 0;
        while ($retryCount <= $this->maxRetries) {
            $ch = curl_init($url);
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

            $result = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

            if ($httpCode == 200) {
                $decodedResult = json_decode($result, true);
                if (isset($decodedResult['data']) && isset($decodedResult['data'][0]['embedding'])) {
                    return $decodedResult['data'][0]['embedding']; // Direkte Rückgabe des Embeddings
                }
            }
        }
        curl_close($ch);

        return null; // Rückgabe von null, falls kein Embedding generiert werden konnte
    }

    private function extractRelevantInfo($data)
    {
        $infoPieces = [];
        if (isset($data['summary'])) {
            $infoPieces[] = $data['summary'];
        }
        if (isset($data['description'])) {
            $infoPieces[] = $data['description'];
        }
        if (isset($data['operationId'])) {
            $infoPieces[] = $data['operationId'];
        }
        return implode(' ', $infoPieces);
    }
}

?>
