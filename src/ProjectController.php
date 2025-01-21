<?php

require_once "DatabaseController.php";

class ProjectController {

    private $connection;

    public function __construct() {
        $this->connection = DatabaseController::connect();
    }

    public function getProjects() {

        try  {
       
            $sql = "SELECT * 
                    FROM murmur
                    WHERE 1";
        
            $statement = $this->connection->prepare($sql);
            $statement->setFetchMode(PDO::FETCH_OBJ);
            $statement->execute();

            $result = $statement->fetchAll();

            return $result;

          } catch(PDOException $error) {
              echo $sql . "<br>" . $error->getMessage();
          }
    }

}