
-- 플립월렛 SQL문 정리

CREATE TABLE `Member` (
    `member_id` UUID NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `login_id` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`member_id`)
);

CREATE TABLE `Total-Goal` (
    `goal_id` UUID NOT NULL,
    `member_id` UUID NOT NULL,
    `total_budget` FLOAT NULL DEFAULT 0.0 CHECK (`total_budget` >= 0),
    `total_expense` FLOAT NULL DEFAULT 0.0 CHECK (`total_expense` >= 0),
    `total_over` FLOAT NULL DEFAULT 0.0 COMMENT,
    `total_remaining` FLOAT NULL DEFAULT 0.0 CHECK (`total_remaining` >= 0) COMMENT 'Derived',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`goal_id`),
    FOREIGN KEY (`member_id`) REFERENCES `Member`(`member_id`)
);

CREATE TABLE `Semi-Goal` (
    `semi_id` UUID NOT NULL,
    `semi_budget` FLOAT NULL DEFAULT 0.0 CHECK (`semi_budget` >= 0),
    `category_id` INT NOT NULL,
    PRIMARY KEY (`semi_id`),
    FOREIGN KEY (`category_id`) REFERENCES `Category`(`category_id`)
);

CREATE TABLE `Category` (
    `category_id` INT NOT NULL,
    `category_name` VARCHAR(255) NOT NULL,
    `category_color` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`category_id`)
);

CREATE TABLE `Semi-Goal Process` (
    `semi_process_id` UUID NOT NULL,
    `member_id` UUID NOT NULL,
    `goal_id` UUID NOT NULL,
    `semi_expense` FLOAT NULL DEFAULT 0.0 CHECK (`semi_expense` >= 0),
    `semi_over` FLOAT NULL DEFAULT 0.0,
    `semi_remaining` FLOAT NULL DEFAULT 0.0 CHECK (`semi_remaining` >= 0),
    `semi_id` UUID NOT NULL,
    PRIMARY KEY (`semi_process_id`),
    FOREIGN KEY (`member_id`) REFERENCES `Member`(`member_id`),
    FOREIGN KEY (`goal_id`) REFERENCES `Total-Goal`(`goal_id`),
    FOREIGN KEY (`semi_id`) REFERENCES `Semi-Goal`(`semi_id`)
);

CREATE TABLE `Surplus` (
    `surplus_id` UUID NOT NULL,
    `goal_id` UUID NOT NULL,
    `member_id` UUID NOT NULL,
    `surplus_budget` FLOAT NULL DEFAULT 0.0 CHECK (`surplus_budget` >= 0),
    `surplus_expense` FLOAT NULL DEFAULT 0.0 CHECK (`surplus_expense` >= 0),
    `surplus_remaining` FLOAT NULL DEFAULT 0.0 CHECK (`surplus_remaining` >= 0),
    PRIMARY KEY (`surplus_id`),
    FOREIGN KEY (`goal_id`) REFERENCES `Total-Goal`(`goal_id`),
    FOREIGN KEY (`member_id`) REFERENCES `Member`(`member_id`)
);

CREATE TABLE `Expense` (
    `expense_id` UUID NOT NULL,
    `semi_id` UUID NOT NULL,
    `goal_id` UUID NOT NULL,
    `member_id` UUID NOT NULL,
    `price` FLOAT NULL DEFAULT 0.0 CHECK (`price` >= 0),
    `item` VARCHAR(255) NULL DEFAULT '',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`expense_id`),
    FOREIGN KEY (`semi_id`) REFERENCES `Semi-Goal Process`(`semi_process_id`),
    FOREIGN KEY (`goal_id`) REFERENCES `Total-Goal`(`goal_id`),
    FOREIGN KEY (`member_id`) REFERENCES `Member`(`member_id`)
);