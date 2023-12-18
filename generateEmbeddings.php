<?php

require 'vendor/autoload.php';
use Dotenv\Dotenv;

// Lade die .env Datei
$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

// OpenAI API-Key aus der .env-Datei
$openai_api_key = $_ENV['OPENAI_API_KEY'];

// Stelle sicher, dass die EmbeddingGenerator-Klasse eingebunden ist
require_once 'EmbeddingGenerator.php';

// Erstelle eine Instanz des EmbeddingGenerators
$embeddingGenerator = new EmbeddingGenerator($openai_api_key);

// Lese die Inhalte der apiEndpoints.json-Datei
$apiEndpointsFilePath = 'apiEndpoints.json'; // Pfad zur apiEndpoints.json
$apiEndpointsContent = file_get_contents($apiEndpointsFilePath);
$apiEndpoints = json_decode($apiEndpointsContent, true); // Konvertiere JSON-Inhalt in ein Array

// Überprüfe, ob das Decoding erfolgreich war
if ($apiEndpoints === null) {
    echo "Fehler beim Decoding der JSON-Daten.";
    exit;
}

// Generiere Embeddings für jeden Endpunkt
$embeddings = $embeddingGenerator->generateEmbeddingsForAPIEndpoints($apiEndpoints['paths']); // Gehe sicher, dass 'paths' der korrekte Key ist

// Speichere die Embeddings in einer Datei
$embeddingsFilePath = 'embeddings.json'; // Pfad, wo die Embeddings gespeichert werden sollen
file_put_contents($embeddingsFilePath, json_encode($embeddings));

echo "Embeddings wurden erfolgreich generiert und gespeichert.";

?>
