Feature: MessageLoop class

    Scenario: logger attribute has default value set
        When MessageLoop instance is created with no arguments
        Then 'messageloop.logger' attribute is set to 'messageit._core.DummyLogger' instance

    Scenario: resolver attribute has default value set
        When MessageLoop instance is created with no arguments
        Then 'messageloop.resolver' attribute is set to 'messageit._core.TypeRegistryResolver' instance

    Scenario: queue attribute is set to queue.Queue instance
        When MessageLoop instance is created with no arguments
        Then 'messageloop.queue' attribute is set to 'queue.Queue' instance

    Scenario: running attribute is set to False
        When MessageLoop instance is created with no arguments
        Then 'messageloop.running' attribute is set to 'False'

    Scenario: stop() method sets running to False
        Given 'FakeMessageLoop' instance with default arguments
        And 'messageloop.running' bool attribute is set to 'True'
        When 'messageloop.stop()' is called
        Then 'messageloop.running' attribute is set to 'False'



