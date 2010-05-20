
function MockBlockRunner(block, fake_tests, max_nb_instructions){
    if (fake_tests !== undefined){
        fake_tests = fake_tests.reverse();
    }
    if (max_nb_instructions === undefined){
        this.max_nb_instructions = 1000;
    }
    else {
        this.max_nb_instructions = max_nb_instructions;
    }
    this.nb_instructions = 0;
    this.block = block;
    this.output = [];
    this.lines_executed = [];
    this.break_loop = false;

    this.execute_command = function(cmd){
        this.output.push(cmd+"()");
    }

    this.on_beeper = function(){
        return fake_tests.pop();
    }

    this.highlight = function(line_number){
        this.lines_executed.push(line_number);
        this.nb_instructions += 1;
        if (this.nb_instructions > this.max_nb_instructions) {
            throw "Too many instructions."
        }
    }

    this.handle_if = function(line){
        this.if_branches = "started";
        this.handle_if_elif(line);
    }

    this.handle_if_elif = function(line){
        var test_result = this.evaluate_condition(line);
        if (test_result && this.if_branches != "done"){
            this.execute_block(line.block);
            this.if_branches = "done";
        }
    }

    this.handle_while = function(line){
        while (true){
            this.highlight(line.line_number);
            test_result = this.evaluate_condition(line);
            if (test_result){
                this.execute_block(line.block);
            }
            else{
                break;
            }

            if( this.break_loop){
                this.break_loop = false;
                break;
            }
        }
    }

    this.evaluate_condition = function(line){
        condition = line.condition;
        if (line.negate_condition){
            condition = !condition;
        }
        if (condition == "on_beeper()") {
            return this.on_beeper();
        }
        return condition;
    }

    this.execute_block = function(block){
        var line;
        for (var i in block.lines){

            if (this.break_loop){  // pop levels until find a loop to break
                break;
            }

            line = block.lines[i];
            if (line.type == "empty line"){
                continue;
            }

            this.highlight(line.line_number);
            if ((line.type == "def block") || (line.type == "assignment")){
               continue;
            }
            else if (line.type == "pass"){
                continue;
            }
            else if (line.type == "user method"){
                this.execute_block(line.block);
            }
            else if (line.type == "command"){
                this.execute_command(line.name);
            }
            else if (line.type == "if block"){
                this.handle_if(line);
            }
            else if (line.type == "elif block"){
                this.handle_if_elif(line);
            }
            else if (line.type == "else block"){
                if (this.if_branches != "done"){
                    this.execute_block(line.block);
                    this.if_branches = "done";
                }
            }
            else if (line.type == "while block"){
                this.handle_while(line);
            }
            else if (line.type == "break"){
                this.break_loop = true;
                break;
            }
            else{
                alert(problem);
                this.output.push("ERROR:" + line.content);
                break;
            }
        }
    }

    try {
        this.execute_block(this.block);
    }
    catch (err) {
        if (err == "Too many instructions.") {
            this.output.push("Too many instructions.");
        }
        else {
            alert("Uncaught exception was raised.")
        }

    }
}